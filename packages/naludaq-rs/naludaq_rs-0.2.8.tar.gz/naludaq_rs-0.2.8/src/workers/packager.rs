//! Worker for splitting board data into events and answers.
//!
//! See the [worker documentation](crate::workers) for information regarding
//! the structure of a worker.
//!
//! # Interface Layer
//! The interface layer for the control worker has some utility functions
//! for retrieving received answers.
//!
//! The stop words must be set before the implementation layer will run.
//!
//! # Control Layer
//! Available commands include setting the stop words and resetting the packager.
//!
//! The implementation layer is started only when the stop words are set.
//!
//! # Implementation Layer
//! The implementation layer reads data from the input channel in a loop
//! and routes events to the [storage worker](crate::workers::storager), while
//! storing answers in a channel for later access.

use std::ops::Range;

use flume::{Receiver, Sender};
use tokio::task::JoinHandle;
use tokio::time::Duration;

use crate::{
    constants::MAX_ANSWER_PACKAGE_SIZE,
    error::PackageWorkerError,
    macros::{try_abort, unwrap_or_break},
    types::{RawAnswer, RawEvent, StopWord},
};

use super::util::{WorkerCommand, WorkerResponse, WorkerResponseHandler};

const DATA_TIMEOUT: Duration = Duration::from_millis(50);

/// A command for the package worker.
///
/// This is sent from the interface layer to the control layer.
#[derive(Clone, Debug)]
enum CommandInner {
    /// Set the stop words used by the packager.
    Start(PackagerConfig),
    /// Resets the package worker.
    ///
    /// This flushes any answers stored in the output channel and
    /// restarts the implementation layer.
    Reset,
    /// Stops the package worker.
    Stop,
}

/// Configuration for the packager.
#[derive(Clone, Debug)]
pub struct PackagerConfig {
    /// Board model
    model: String,
    /// Stop word for events.
    event_stop_word: StopWord,
    /// Stop word for answers.
    answer_stop_word: StopWord,
}

impl PackagerConfig {
    /// Create a new packager configuration.
    pub fn new<S: AsRef<str>>(
        model: S,
        event_stop_word: StopWord,
        answer_stop_word: StopWord,
    ) -> Self {
        PackagerConfig {
            model: model.as_ref().to_string(),
            event_stop_word,
            answer_stop_word,
        }
    }

    /// Returns the model name used by the packager.
    pub fn model(&self) -> &str {
        &self.model
    }

    /// Returns the event stop word.
    pub fn event_stop_word(&self) -> &StopWord {
        &self.event_stop_word
    }

    /// Returns the answer stop word.
    pub fn answer_stop_word(&self) -> &StopWord {
        &self.answer_stop_word
    }
}

/// A response to a [`Command`].
///
/// This is sent from the control layer to the interface layer.
type ResponseInner = Result<(), PackageWorkerError>;

/// Interface layer for the package worker.
///
/// The stop words must be set before any packages can be received.
#[derive(Clone, Debug)]
pub struct PackageWorker {
    /// Control-side channel for commands send to the worker.
    command_rx: Receiver<WorkerCommand<CommandInner>>,
    /// Control-side channel for command responses.
    response_tx: Sender<WorkerResponse<ResponseInner>>,
    /// Implementation-side output channel for events.
    events_tx: Sender<RawEvent>,
    /// Implementation-side output channel for answers
    answers_tx: Sender<RawAnswer>,
    /// Input channel for data received by the [connection worker](crate::workers::connection)
    data_rx: Receiver<Vec<u8>>,
    /// Handler for responses from the implementation layer.
    response_handler: WorkerResponseHandler<CommandInner, ResponseInner>,
}

impl PackageWorker {
    /// Create a new package worker.
    ///
    /// All data received by `data_rx` will be packaged, and any events found
    /// are sent through `events_tx`.
    ///
    /// The worker should be run with the `start()` method before
    /// performing any operations.
    pub fn new(data_rx: Receiver<Vec<u8>>, events_tx: Sender<RawEvent>, answer_tx: Sender<RawAnswer>) -> Self {
        let (command_tx, command_rx) = flume::unbounded();
        let (response_tx, response_rx) = flume::unbounded();

        PackageWorker {
            command_rx,
            response_tx,
            answers_tx: answer_tx,
            events_tx,
            data_rx,
            response_handler: WorkerResponseHandler::new(command_tx, response_rx),
        }
    }

    /// Runs the worker. This method will run indefinitely until the worker is stopped.
    pub async fn start(&self) {
        let command_rx = self.command_rx.clone();
        let response_tx = self.response_tx.clone();
        let data_rx = self.data_rx.clone();
        let events_tx = self.events_tx.clone();
        let answers_tx = self.answers_tx.clone();
        run_packager_task_controller(command_rx, response_tx, data_rx, answers_tx, events_tx).await;
    }

    /// Stops the worker. This method will not return until the control layer halts.
    pub async fn stop(&self) {
        let _ = self.request(CommandInner::Stop).await;
    }

    /// Sets the stop words used by the packager.
    ///
    /// This will run or restart the implementation layer.
    pub async fn set_configuration(&self, config: PackagerConfig) {
        self.request(CommandInner::Start(config)).await.unwrap();
    }

    /// Resets the packager.
    ///
    /// This will clear any received answers and restart the
    /// implementation layer.
    ///
    /// Requires the implementation layer to already be started.
    pub async fn reset(&self) -> Result<(), PackageWorkerError> {
        self.request(CommandInner::Reset).await
    }

    /// Sends a [`Command`] to the control layer, and
    /// returns a [`Response`] indicating the operation status.
    async fn request(&self, command: CommandInner) -> ResponseInner {
        self.response_handler
            .request(command)
            .await
            .expect("package worker request failed; the channels were dropped")
    }
}

/// Control layer for the package worker.
///
/// Yields until the next command is received in the `command_rx` channel, then processes
/// the command and returns a response in the `response_tx` channel.
///
/// Data to package is received in the `data_rx` channel, and answers and events
/// and sent through the corresponding output channels.
#[tracing::instrument(skip_all)]
async fn run_packager_task_controller(
    command_rx: Receiver<WorkerCommand<CommandInner>>,
    response_tx: Sender<WorkerResponse<ResponseInner>>,
    data_rx: Receiver<Vec<u8>>,
    answers_tx: Sender<RawAnswer>,
    events_tx: Sender<RawEvent>,
) {
    let mut handle: Option<JoinHandle<()>> = None;
    let mut config: Option<PackagerConfig> = None;

    loop {
        let WorkerCommand(id, command) = unwrap_or_break!(command_rx.recv_async().await);
        let response = match command {
            CommandInner::Start(new_config) => {
                tracing::debug!("Starting packager: {new_config:?}");
                try_abort!(handle);
                config = Some(new_config.clone());
                handle = Some(tokio::spawn(run_packager_impl(
                    data_rx.clone(),
                    answers_tx.clone(),
                    events_tx.clone(),
                    new_config,
                )));
                Ok(())
            }
            CommandInner::Reset => {
                data_rx.drain();
                match config {
                    Some(ref config) => {
                        try_abort!(handle);
                        handle = Some(tokio::spawn(run_packager_impl(
                            data_rx.clone(),
                            answers_tx.clone(),
                            events_tx.clone(),
                            config.clone(),
                        )));
                        Ok(())
                    }
                    None => Err(PackageWorkerError::NotInitialized),
                }
            }
            CommandInner::Stop => {
                tracing::debug!("Trying to stop package worker");
                try_abort!(handle);
                response_tx.send(WorkerResponse(id, Ok(()))).unwrap();
                break;
            }
        };
        unwrap_or_break!(response_tx.send(WorkerResponse(id, response)));
    }
}

/// Implementation layer for the package worker.
///
/// Continually packages received data and sends events/answers to the output channels.
/// If an error occurs while receiving from the input channel, the function immediately returns.
#[tracing::instrument(skip_all)]
async fn run_packager_impl(
    data_rx: Receiver<Vec<u8>>,
    answers_tx: Sender<Vec<u8>>,
    events_tx: Sender<Vec<u8>>,
    config: PackagerConfig,
) {
    let _ = data_rx.drain();
    tracing::debug!("Running package worker with config: {config:?}");

    if hdsoc::MODELS.contains(&config.model.as_ref()) {
        tracing::debug!("SELECTING HDSOC PACKAGER");
        hdsoc::packager_loop(data_rx, events_tx, answers_tx, config).await
    } else {
        tracing::debug!("SELECTING DEFAULT PACKAGER");
        packager_loop_default(data_rx, events_tx, answers_tx, config).await
    }
}

/// Default implementation of the package worker.
async fn packager_loop_default(
    data_rx: Receiver<Vec<u8>>,
    events_tx: Sender<RawEvent>,
    answers_tx: Sender<RawAnswer>,
    config: PackagerConfig,
) {
    let mut accumulated_data = Vec::new();
    let mut start_index = 0;
    while !data_rx.is_disconnected() {
        // Yielding is super necessary to avoid freezing the server!
        tokio::task::yield_now().await;
        await_data(&data_rx, &mut accumulated_data, DATA_TIMEOUT).await;
        if accumulated_data.len() == 0 {
            continue;
        }

        if let Some((packages, consumed_bytes)) = packages(&accumulated_data, &config, start_index)
        {
            accumulated_data.drain(..consumed_bytes);
            packages.answers.iter().for_each(|ans| {
                tracing::debug!("Answer: {ans:?}");
            });
            send_packages(packages.answers, &answers_tx);
            send_packages(packages.events, &events_tx);
        }
        start_index = accumulated_data.len();
    }
    tracing::debug!("Package worker stopped");
}

/// Wait for data to arrive in the data channel, and append it to to the given output buffer.
/// All data data sitting in the channel will be extracted.
///
/// In the event the data channel is disconnected, the function returns immediately
/// and does not append any data to the buffer.
async fn await_data(data_rx: &Receiver<Vec<u8>>, buf: &mut Vec<u8>, wait_duration: Duration) {

    match tokio::time::timeout(wait_duration, data_rx.recv_async()).await {
        Ok(Ok(data)) => {
            // if we got one package there is a good chance we have a bunch more,
            // so might as well pull them all out at once
            buf.extend(data.into_iter().chain(data_rx.drain().flatten()));
        },
        Ok(Err(_)) => {
            // The channel was disconnected, so return immediately
            tracing::warn!("Channel disconnected");
        },
        Err(_) => {
            // The timeout reached
            // tracing::warn!("Timed out waiting for data");
        }

    }
}

/// Send the given packages through the given channel.
///
/// Any errors which occur during sending are ignored.
fn send_packages(packages: Vec<RawAnswer>, tx: &Sender<RawAnswer>) {
    packages.into_iter().for_each(|pkg| {
        let _ = tx.send(pkg);
    });
}

/// Search the data for packages (either answers or events) and return all the stop word indexes.
///
/// The `start_index` is the location in the data to begin looking for stop words.
/// This is useful to avoid searching the data multiple times for stop words
/// while accumulating a large event.
///
/// This turns out to be a fairly tricky problem when considering all the edge cases:
/// - There are two stop words, which may be different in the general case
/// - The stop words may be of different lengths
/// - The event stop word (e.g. FACECAFE) might contain the answer stop word (e.g. FACE), and vice versa
///
/// Returns (answer_package_locations, event_package_locations, total_bytes_consumed)
fn package_locations(
    data: &[u8],
    config: &PackagerConfig,
    mut start_index: usize,
) -> (Vec<Range<usize>>, Vec<Range<usize>>, usize) {
    let event_stop_word = &config.event_stop_word;
    let answer_stop_word = &config.answer_stop_word;
    // Need to start slightly earlier since the stop word may be split across two
    // calls to this function. Happens every single time with UPAC96 & D3XX 😢
    start_index = start_index.saturating_sub(std::cmp::max(event_stop_word.len(), answer_stop_word.len()));

    let is_event_stop_word =
        |i| matches!(data.get(i..i+event_stop_word.len()), Some(x) if x == event_stop_word);
    let is_answer_stop_word =
        |i| matches!(data.get(i..i+answer_stop_word.len()), Some(x) if x == answer_stop_word);

    let mut pkg_start = 0;
    let mut answer_locations = Vec::new();
    let mut event_locations = Vec::new();
    for i in start_index..data.len() {
        let pkg_len = i.saturating_sub(pkg_start) + answer_stop_word.len();
        let (buf, pkg_end) = if is_event_stop_word(i) && pkg_len > MAX_ANSWER_PACKAGE_SIZE {
            (&mut event_locations, i + event_stop_word.len())
        } else if is_answer_stop_word(i) && pkg_len <= MAX_ANSWER_PACKAGE_SIZE {
            (&mut answer_locations, i + answer_stop_word.len())
        } else {
            continue;
        };
        buf.push(pkg_start..pkg_end);
        pkg_start = pkg_end;
    }
    let bytes_consumed = pkg_start; // rebind is just for clarity
    (answer_locations, event_locations, bytes_consumed)
}

/// Split the data into event and answer packages based on the given config.
///
/// Takes a `start_index` which allows the function to start searching for packages
/// at a specific index. This is useful to avoid searching the same data multiple
/// times while accumulating a large event.
///
/// Returns the packages and the number of bytes consumed from the data.
fn packages(data: &[u8], config: &PackagerConfig, start_index: usize) -> Option<(Packages, usize)> {
    let (answer_locations, event_locations, bytes_consumed) =
        package_locations(data, config, start_index);
    let mut packages = Packages::with_capacities(answer_locations.len(), event_locations.len());
    let extract = |locs: Vec<Range<usize>>| locs.into_iter().map(|range| data[range].to_vec());
    packages.answers.extend(extract(answer_locations));
    packages.events.extend(extract(event_locations));
    Some((packages, bytes_consumed))
}

/// Storage for event and answer packages.
struct Packages {
    answers: Vec<RawAnswer>,
    events: Vec<RawEvent>,
}

impl Packages {
    /// Create a new `Packages` struct with the given capacities
    /// for the answer and event data vectors.
    pub fn with_capacities(answers: usize, events: usize) -> Self {
        Self {
            answers: Vec::with_capacity(answers),
            events: Vec::with_capacity(events),
        }
    }
}

/// Packager implementation for the HDSoC.
///
/// HDSoC has no built-in concept of events, so it needs a custom implementation.
/// Each window is sent individually with its own stop word. In this implementation
/// an event is built up from multiple windows based on their respective timing fields.
/// The boundary between events is defined by the difference between the timing fields
/// and a hardcoded maximum margin of timing.
mod hdsoc {
    use std::time::{Duration, Instant};

    use flume::{Receiver, Sender};

    use super::{await_data, packages, send_packages, PackagerConfig};
    use crate::types::{RawAnswer, RawEvent};

    pub const MODELS: [&str; 2] = ["hdsocv1_evalr2", "hdsocv2_eval"];

    /// Bitmask for extracting the timing field for windows
    const TIMING_MASK: u16 = 0xFFF;
    /// Bitshift amount for the most significant portion of the timing field
    const TIMING_SHIFT: u8 = 12;
    /// Maximum amount that window timings are allowed to differ within an event.
    /// This value is experimentally determined.
    ///
    /// This value is the main factor in determining how to group windows into events.
    /// It is theoretically possible to have two different events back-to-back with timings
    /// that are within this margin, but it's unlikely to happen in practice.
    const TIMING_MARGIN: u16 = 1500;
    /// Maximum time to wait between windows before flushing the last event.
    ///
    /// This doesn't really need to be a specific value since it's only used
    /// when events have stopped being sent back. That being said, don't set
    /// it too high or the last event could get stuck and not written, and
    /// don't set it too low or single events could be split into multiple.
    const TIMEOUT: Duration = Duration::from_millis(50);
    const DATA_TIMEOUT: tokio::time::Duration = tokio::time::Duration::from_millis(50);
    /// Offset in bytes of the timing field in a window.
    const TIMING_FIELD_OFFSET: usize = 2;

    /// Type alias for window data in an event.
    type Window = Vec<u8>;

    /// Simple error type to indicate when timings are mismatched in the event builder.
    #[derive(thiserror::Error, Debug)]
    enum EventBuilderError {
        /// Tried to insert a window with a timing difference outside the margin.
        #[error("window timings differ by too much to store in the event")]
        WindowTimingMismatched,
        /// The window cannot be inserted because it is invalid data.
        #[error("window is invalid")]
        InvalidWindow,
    }

    /// Builder for HDSoC events. Accumulates many windows into a single event.
    #[derive(Debug, Clone)]
    struct EventBuilder {
        /// Timing field of the very first window
        timing: Option<u16>,
        /// Flat collection of all windows received so far.
        data: Vec<u8>,
    }

    impl EventBuilder {
        /// Create an empty event builder with unspecified timing.
        ///
        /// The timing field will be set when the first window is inserted.
        fn new() -> Self {
            Self {
                timing: None,
                data: Vec::new(),
            }
        }

        /// Attempts to insert the given window into the event.
        ///
        /// # Errors
        /// * [`EventBuilderError::WindowTimingMismatched`] if the timing field on the given window
        ///   differs from the timing field on the first window by more than [`TIMING_MARGIN`].
        /// * [`EventBuilderError::InvalidWindow`] if the given window is invalid.
        fn try_insert_window(&mut self, window: &Window) -> Result<(), EventBuilderError> {
            // Compute the absolute difference in the timing field since the first packet
            let window_timing = window_timing(window)?;
            let event_timing = *self.timing.get_or_insert(window_timing);
            let offset = (window_timing as isize - event_timing as isize).abs();

            if offset as u16 <= TIMING_MARGIN {
                self.data.extend(window);
                Ok(())
            } else {
                Err(EventBuilderError::WindowTimingMismatched)
            }
        }

        /// Resets the builder and returns the built event, if any.
        #[inline]
        fn reset(&mut self) -> Option<RawEvent> {
            self.timing = None;
            if self.data.is_empty() {
                None
            } else {
                Some(std::mem::take(&mut self.data))
            }
        }

        /// Resets the builder and inserts the given window as the first window.
        /// If the given window is invalid, the builder will not be initialized.
        ///
        /// Returns the built event, if any.
        #[inline]
        fn reset_with_initial_window(&mut self, window: Window) -> Option<RawEvent> {
            let result = self.reset();
            let _ = self.try_insert_window(&window);
            result
        }
    }

    /// Parses the timing field of the given window.
    ///
    /// Errors:
    /// * [`EventBuilderError::InvalidWindow`] if the window is too short to contain the timing field.
    #[inline]
    fn window_timing(window: &Window) -> Result<u16, EventBuilderError> {
        if window.len() < TIMING_FIELD_OFFSET + 4 {
            return Err(EventBuilderError::InvalidWindow);
        }
        let upper_bytes = TIMING_FIELD_OFFSET..TIMING_FIELD_OFFSET + 2;
        let lower_bytes = TIMING_FIELD_OFFSET + 2..TIMING_FIELD_OFFSET + 4;
        // SAFETY: safe to unwrap try_into() since the length of the slices
        // will always be correct.
        let upper = u16::from_be_bytes(window[upper_bytes].try_into().unwrap());
        let lower = u16::from_be_bytes(window[lower_bytes].try_into().unwrap());
        Ok(((upper & TIMING_MASK) << TIMING_SHIFT) | (lower & TIMING_MASK))
    }

    /// Packager loop for HDSoC.
    ///
    /// Packages data received from the `data_rx` channel and sends the resulting events and
    /// answers to the `events_tx` and `answers_tx` channels respectively.
    pub async fn packager_loop(
        data_rx: Receiver<Vec<u8>>,
        events_tx: Sender<RawEvent>,
        answers_tx: Sender<RawAnswer>,
        config: PackagerConfig,
    ) {
        let mut start_index = 0;
        let mut accumulated_data = Vec::new();
        let mut last_packet_time = Instant::now();
        let mut current_event = EventBuilder::new();

        while !data_rx.is_disconnected() {
            // Yielding is super necessary to avoid freezing the server!
            // tokio::task::yield_now().await;
            await_data(&data_rx, &mut accumulated_data, DATA_TIMEOUT).await;

            // Timeout logic to prevent the last event in a readout from getting stuck
            if Instant::now() - last_packet_time > TIMEOUT {
                if let Some(event) = current_event.reset() {
                    let _ = events_tx.send(event);
                }
            }
            last_packet_time = Instant::now();

            if accumulated_data.len() == 0 {
                continue;
            }

            let packages = match packages(&accumulated_data, &config, start_index) {
                Some((packages, consumed_bytes)) => {
                    accumulated_data.drain(..consumed_bytes);
                    packages
                }
                None => continue,
            };

            start_index = accumulated_data.len();

            packages.events.into_iter().for_each(|window| {
                match current_event.try_insert_window(&window) {
                    Err(EventBuilderError::WindowTimingMismatched) => {
                        // SAFETY: safe to unwrap since `try_insert_window` only fails if
                        // there is an event to return.
                        let event = current_event.reset_with_initial_window(window).unwrap();
                        let _ = events_tx.send(event);
                    }
                    _ => {}
                }
            });
            send_packages(packages.answers, &answers_tx);
        }

        tracing::debug!("HDSoC packager stopped");
    }
}
