//! Library for the NaluDAQ backend.
//!
//! The backend is a web server which provides several
//! HTTP routes for interacting with the board and data.
//!
//! # Library Structure
//! The are two main parts to the backend: the server, and the workers.
//!
//! ## Workers
//! [Workers](crate::workers) run a specific task continuously, and communicate with each other
//! using [flume] channels. There are currently three types of workers:
//! - the [connection worker](crate::workers::connection::ConnectionWorker), which read/writes raw data through a
//!   [`Connection`](crate::connection::Connection);
//! - the [package worker](crate::workers::packager::PackageWorker), which separates raw data from the connection into events and answers;
//! - and the [storage worker](crate::workers::storager::StorageWorker), which stores events to disk.
//!
//! For more details, see the [worker documentation](crate::workers)
//!
//! ## Server
//! The server handles communication and configuration through a REST API built atop [axum].
//!
//! The REST API may be viewed by running the following command:
//! ```sh
//! $ cargo run --bin api
//! ```
//!
//! For more details, see the [server documentation](crate::web_api).

pub mod bindings;
pub mod connection;
pub mod constants;
pub mod error;
pub mod macros;
pub mod types;
pub mod web_api;
pub mod workers;
