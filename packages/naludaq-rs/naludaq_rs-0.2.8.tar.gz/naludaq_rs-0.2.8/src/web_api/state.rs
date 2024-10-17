//! Module containing a shared representation of the server state.
//!
//! The [`ServerState`] struct stores useful values which endpoints can
//! use to manipulate the server and its workers.

use std::{path::PathBuf};

use crate::workers::Workers;

/// A collection of values which are important for interacting with the server.
#[derive(Clone, Debug)]
pub struct ServerState {
    /// Root directory for this server.
    root: PathBuf,
    /// Collection of workers running in the server.
    workers: Workers,
}

impl ServerState {
    /// Create a new [`ServerState`] under the given root directory.
    ///
    /// The workers are not started by this method.
    pub fn new(root: PathBuf) -> ServerState {
        Self {
            root: root.clone(),
            workers: Workers::new(root),
        }
    }

    /// Get the workers running under the server.
    pub fn workers(&self) -> &Workers {
        &self.workers
    }

    /// Get the root directory for the server.
    pub fn root(&self) -> &PathBuf {
        &self.root
    }
}
