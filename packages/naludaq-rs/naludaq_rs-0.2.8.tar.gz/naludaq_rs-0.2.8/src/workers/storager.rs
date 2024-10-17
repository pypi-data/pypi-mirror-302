//! Worker for storing events received from the [package worker](crate::workers::packager)
//! to an acquisition on disk.
//!
//! See the [worker documentation](crate::workers) for information regarding
//! the structure of a worker.
//!
//! # Interface Layer
//! The interface layer for worker allows the user to set the target acquisition.
//!
//! The target acquisition must be set before the implementation layer will run.
//!
//! # Control Layer
//! Available commands include getting/setting the target acquistiion.
//!
//! The implementation layer is started only when the target is set.
//!
//! # Implementation Layer
//! The implementation layer reads events from the input channel in a loop
//! and writes events to disk as they come in.

use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};

use flume::{Receiver, Sender};
use naluacq::Acquisition;
use naluacq::acquisition::chunk::{WriteChunkFile, WriteChunkFileBuilder};

use crate::constants::{
    ENABLE_STORAGE_SPEED_LOGGING, STORAGE_FLUSH_TIMEOUT, STORAGE_POLLING_INTERVAL,
};
use crate::{error::StorageWorkerError, macros::try_abort};
use crate::{macros::unwrap_or_break, types::RawEvent};

use super::util::{WorkerCommand, WorkerResponse, WorkerResponseHandler};

/// A command for the storage worker.
///
/// This is sent from the interface layer to the control layer.
#[derive(Clone, Debug)]
enum CommandInner {
    /// Change the target acquisition. If the acquisition name is `None`,
    /// the implementation layer is stopped.
    SetOutput { name: Option<String> },
    /// Get the name of the target acquisition
    GetOutput,
    /// Stops the worker.
    Stop,
}

/// A response to a [`Command`].
///
/// This is sent from the control layer to the interface layer.
#[derive(Clone, Debug)]
enum ResponseInner {
    /// The name of the target acquisition. Sent in response to a
    /// [`Command::GetOutput`] command.
    OutputName(Option<String>),
    /// No response necessary for the given [`Command`]
    None,
}

/// A response to a [`Command`].
///
/// This is sent from the control layer to the interface layer.
type ResponseResult = Result<ResponseInner, StorageWorkerError>;

#[derive(Clone, Debug)]

/// Interface layer for the storage worker.
///
/// The target acquisition must be set before any events are written to disk.
pub struct StorageWorker {
    /// Directory where all acquistions are stored.
    root: PathBuf,
    /// Control-side channel for commands send to the worker.
    command_rx: Receiver<WorkerCommand<CommandInner>>,
    /// Control-side channel for command responses.
    response_tx: Sender<WorkerResponse<ResponseResult>>,
    /// Input channel for events sent by the [package worker](crate::workers::packager).
    events_rx: Receiver<RawEvent>,
    /// Handler for responses from the implementation layer.
    response_handler: WorkerResponseHandler<CommandInner, ResponseResult>,
}

impl StorageWorker {
    /// Create a new storage worker.
    ///
    /// All events received by `data_rx` are written to the target acquisition
    /// living under the `root` directory.
    pub fn new(root: PathBuf, events_rx: Receiver<RawEvent>) -> Self {
        let (command_tx, command_rx) = flume::unbounded();
        let (response_tx, response_rx) = flume::unbounded();

        StorageWorker {
            root,
            command_rx,
            response_tx,
            events_rx,
            response_handler: WorkerResponseHandler::new(command_tx, response_rx),
        }
    }

    /// Runs the worker. This method will run indefinitely until the worker is stopped.
    pub async fn start(&self) {
        let command_rx = self.command_rx.clone();
        let response_tx = self.response_tx.clone();
        let events_rx = self.events_rx.clone();
        let root = self.root.clone();
        run_storager_task_controller(command_rx, response_tx, events_rx, root).await;
    }

    /// Stops the worker. This method will not return until the control layer halts.
    pub async fn stop(&self) {
        let _ = self.request(CommandInner::Stop).await;
    }

    /// Gets the name of the target acquisition.
    ///
    /// [`None`] is returned if the target is not set.
    pub async fn output(&self) -> Option<String> {
        match self
            .request(CommandInner::GetOutput)
            .await
            .expect("failed to get current output")
        {
            ResponseInner::OutputName(name) => name,
            _ => None,
        }
    }

    /// Set the target acquisition to the given name.
    ///
    /// All further events received will be stored to this target.
    ///
    /// For this to work, the acquisition indicated by `Some(name)` must be an existing
    /// acquisition. If `None` is provided, disk writing is stopped.
    pub async fn set_output(&self, name: Option<String>) -> Result<(), StorageWorkerError> {
        self.request(CommandInner::SetOutput { name }).await?;
        Ok(())
    }

    // Sends a [`Command`] to the control layer, and
    /// returns a [`Response`] indicating the operation status.
    async fn request(&self, command: CommandInner) -> ResponseResult {
        self.response_handler
            .request(command)
            .await
            .expect("storage worker request failed; the channels were dropped")
    }
}

/// Control layer for the storage worker.
///
/// Yields until the next command is received in the `command_rx` channel, then processes
/// the command and returns a response in the `response_tx` channel.
///
/// Events to write are received through the `events_rx` channel. All acquisitions
/// are accessed relative to the `root` directory.
#[tracing::instrument(skip_all)]
async fn run_storager_task_controller(
    // slave: Slave<StoragerWorkerCommand, StoragerWorkerResponse>,
    command_rx: Receiver<WorkerCommand<CommandInner>>,
    response_tx: Sender<WorkerResponse<ResponseResult>>,
    events_rx: Receiver<RawEvent>,
    root: PathBuf,
) {
    let mut handle = None;
    let mut current_acq: Option<Acquisition> = None;
    let mut cancel_token = Arc::new(AtomicBool::new(false));

    loop {
        let WorkerCommand(id, command) = unwrap_or_break!(command_rx.recv_async().await);
        let response = match command {
            CommandInner::GetOutput => Ok(ResponseInner::OutputName(
                current_acq.clone().map(|acq| acq.name()),
            )),
            CommandInner::SetOutput { name: Some(name) } => {
                tracing::debug!("Changing output acquisition to: {:?}", name);
                events_rx.drain();
                match Acquisition::open(root.join(name)) {
                    Ok(acq) => {
                        current_acq = Some(acq.clone());
                        cancel_token.store(true, Ordering::Relaxed);
                        cancel_token = Arc::new(AtomicBool::new(false));
                        let cancel_token = cancel_token.clone();
                        let events_rx = events_rx.clone();
                        handle = Some(tokio::task::spawn_blocking(move || {
                            run_storager_impl(events_rx, acq, cancel_token)
                        }));
                        Ok(ResponseInner::None)
                    }
                    Err(e) => {
                        tracing::error!("Could not open acquisition for writing: {e:?}");
                        Err(StorageWorkerError::InvalidPath)
                    }
                }
            }
            CommandInner::SetOutput { name: None } => {
                tracing::debug!("Stopping acquisition output");
                cancel_token.store(true, Ordering::Relaxed);
                current_acq = None;
                try_abort!(handle);
                handle = None;
                Ok(ResponseInner::None)
            }
            CommandInner::Stop => {
                tracing::debug!("Stopping storage worker");
                try_abort!(handle);
                response_tx
                    .send(WorkerResponse(id, Ok(ResponseInner::None)))
                    .unwrap();
                break;
            }
        };

        unwrap_or_break!(response_tx.send(WorkerResponse(id, response)));
    }
}

/// Implementation layer for the storage worker.
///
/// Continually writes data to the target acquisition.
#[tracing::instrument(skip_all)]
fn run_storager_impl(
    events_rx: Receiver<Vec<u8>>,
    acq: Acquisition,
    cancel_token: Arc<AtomicBool>,
) {
    tracing::debug!("Running storager for root: {:?}", acq.name());

    // Drain leftover events from the channel
    let _ = events_rx.drain().count();

    let mut chunk_count = 0;
    let mut chunk: Option<WriteChunkFile> = None; // chunk created after first event received
    let mut last_event_time = Instant::now();

    // debug variables
    let mut num_bytes_received = 0;
    let mut last_speed_print_time = Instant::now();
    let speed_print_interval = Duration::from_millis(1000);

    loop {
        if cancel_token.load(Ordering::Relaxed) {
            tracing::debug!("Received shutdown request for storager worker");
            break;
        }
        if events_rx.is_disconnected() {
            break;
        }
        if events_rx.is_empty() {
            if Instant::now() - last_event_time > STORAGE_FLUSH_TIMEOUT
                && chunk.is_some()
                && chunk.as_ref().unwrap().unwritten_amount() != 0
            {
                tracing::debug!("No event received within timeout; flushing chunk");
                match chunk.as_mut().unwrap().truncate() {
                    Ok(()) => (),
                    Err(e) => {
                        tracing::debug!("Unable to truncate chunk due to {e:?}");
                        break;
                    }
                }
            }

            std::thread::sleep(STORAGE_POLLING_INTERVAL);
            continue;
        }

        for event in events_rx.drain().collect::<Vec<RawEvent>>() {
            last_event_time = Instant::now();
            num_bytes_received += event.len();

            // Ensure that we have a writable chunk
            // This code is Rust anti-pattern, but it helps avoid super-nested match blocks and repetitive code
            if chunk.is_some() && !chunk.as_mut().unwrap().can_fit(&event) {
                chunk = None;
            }
            if chunk.is_none() {
                chunk = match WriteChunkFileBuilder::new()
                    .metadata(&acq.metadata_str().expect("acquisition metadata is unreadable"))
                    .open(acq.path(), chunk_count)
                {
                    Ok(chunk) => {
                        chunk_count += 1;
                        Some(chunk)
                    }
                    Err(e) => {
                        tracing::error!("Failed to open next chunk file: {e:?}");
                        break;
                    }
                }
            };

            // Write the event to the chunk
            match chunk.as_mut().unwrap().write(event) {
                Ok(()) => (),
                Err(e) => {
                    tracing::error!("Failed to write data to chunk {chunk_count}: {e:?}");
                    break;
                }
            }
        }

        // debug stuff
        if ENABLE_STORAGE_SPEED_LOGGING {
            let elapsed = Instant::now() - last_speed_print_time;
            if elapsed > speed_print_interval {
                tracing::debug!(
                    "Storager speed={} KB/s, unwritten amount={} KB",
                    (num_bytes_received as f64 / elapsed.as_secs_f64() / 1_000f64) as u32,
                    chunk.as_mut().unwrap().unwritten_amount() / 1_000
                );
                last_speed_print_time = Instant::now();
                num_bytes_received = 0;
            }
        }
    }
}
