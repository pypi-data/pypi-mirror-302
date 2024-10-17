//! Module containing all the workers.
//!
//! There are three workers:
//! - the [connection worker](crate::workers::connection), which read/writes raw data through a
//!   [`Connection`](crate::connection::Connection);
//! - the [package worker](crate::workers::packager), which separates raw data from the connection into events and answers;
//! - and the [storage worker](crate::workers::storager), which stores events to disk.
//!
//! # Parts of a Worker
//!
//! Each type of worker lives in its own module, and is made up of three parts.
//!
//! The **implementation** layer does the heavy lifting. This function
//! is not executed straight away when the worker starts, but is instead executed when
//! the worker is (re)configured. The implementation function may be started/stopped at any
//! point.
//!
//! The **control** layer is another function which interprets commands received over a
//! [`flume`] channel, holds configuration values, and controls when the implementation
//! function runs and in which context it runs.
//!
//! The **interface** layer is a struct which provides a tidy API over the control layer
//! by sending commands/receiving answers to/from the control layer. The interface layer
//! also provides start/stop functions.

use std::path::PathBuf;

use self::{
    answers::AnswerWorker, connection::ConnectionWorker, packager::PackageWorker,
    storager::StorageWorker,
};
use crate::{error::WorkerError, types::RawCommand};

pub mod answers;
pub mod connection;
pub mod packager;
pub mod storager;
mod util;

/// A simple container holding the interface layers for each worker.
#[derive(Clone, Debug)]
pub struct Workers {
    /// The connection worker interface.
    connection: ConnectionWorker,
    /// The package worker interface.
    package: PackageWorker,
    /// The storage worker interface.
    storage: StorageWorker,
    /// The answer worker interface.
    answer: AnswerWorker,
}

impl Workers {
    /// Instantiate the workers.
    ///
    /// The `root` path is the root directory of the [storage worker](`StorageWorker`).
    ///
    /// This function does not start the workers.
    pub fn new(root: PathBuf) -> Self {
        let (from_board_tx, from_board_rx) = flume::unbounded();
        let (events_tx, events_rx) = flume::unbounded();
        let (answer_tx, answer_rx) = flume::unbounded();

        let connection = ConnectionWorker::new(from_board_tx);
        let package = PackageWorker::new(from_board_rx, events_tx, answer_tx);
        let storage = StorageWorker::new(root, events_rx);
        let answer = AnswerWorker::new(answer_rx);

        Workers {
            connection,
            package,
            storage,
            answer,
        }
    }

    /// Runs all of the workers simultaneously.
    ///
    /// This function will not return until all the workers have stopped.
    #[tracing::instrument(skip_all)]
    pub async fn run(&self) {
        tracing::info!("Starting workers");
        futures::join!(
            self.connection.start(),
            self.package.start(),
            self.storage.start(),
            self.answer.start(),
        );
    }

    /// Stops all of the workers simultaneously.
    ///
    /// This function will not return until all the workers have stopped.
    pub async fn stop(&self) {
        futures::join!(
            self.connection.stop(),
            self.package.stop(),
            self.storage.stop()
        );
    }

    /// Convenience function for sending a write command to the board.
    ///
    /// # Errors
    /// A [`WorkerError`] is returned if the command could not be sent.
    pub async fn send_write_command(&self, command: RawCommand) -> Result<(), WorkerError> {
        Ok(self.connection_worker().send_command(command).await?)
    }

    /// Convenience function for sending several write commands to the board.
    ///
    /// # Errors
    /// A [`WorkerError`] is returned if the command could not be sent.
    pub async fn send_write_commands(&self, commands: Vec<RawCommand>) -> Result<(), WorkerError> {
        for command in commands {
            self.send_write_command(command).await?;
        }
        Ok(())
    }

    /// Gets the connection worker.
    #[inline]
    pub fn connection_worker(&self) -> &ConnectionWorker {
        &self.connection
    }

    /// Gets the package worker.
    #[inline]
    pub fn package_worker(&self) -> &PackageWorker {
        &self.package
    }

    /// Gets the storage worker.
    #[inline]
    pub fn storage_worker(&self) -> &StorageWorker {
        &self.storage
    }

    /// Gets a mutable reference to the connection worker.
    #[inline]
    pub fn connection_worker_mut(&mut self) -> &mut ConnectionWorker {
        &mut self.connection
    }

    /// Gets a mutable reference to the package worker.
    #[inline]
    pub fn package_worker_mut(&mut self) -> &mut PackageWorker {
        &mut self.package
    }

    /// Gets a mutable reference to the storage worker.
    #[inline]
    pub fn storage_worker_mut(&mut self) -> &mut StorageWorker {
        &mut self.storage
    }

    /// Gets a reference to the answer worker.
    #[inline]
    pub fn answer_worker(&self) -> &AnswerWorker {
        &self.answer
    }
}
