//! Module containing all error types used by the backend.

/// Errors used by the [connection worker](crate::workers::connection).
#[derive(thiserror::Error, Debug, Clone)]
pub enum ConnectionWorkerError {
    /// Attempted to send data without a connection
    #[error("there is no connection")]
    NoConnection,
    /// Could not open the connection.
    #[error("failed to open a connection")]
    ConnectionFailed,
    /// Could not send data to the board.
    #[error("failed to send data to board")]
    SendFailed,
}

/// Errors used by the [package worker](crate::workers::packager).
#[derive(thiserror::Error, Debug, Clone)]
pub enum PackageWorkerError {
    /// Attempted to reset the packager without initializing it first.
    #[error("packager not initialized")]
    NotInitialized,
}

/// Errors used by the [package worker](crate::workers::packager).
#[derive(thiserror::Error, Debug, Clone)]
pub enum AnswerWorkerError {
    /// Failed to receive a response from the board in time.
    #[error("failed to receive data from the board in time")]
    ReceiveTimeout,
    /// Failed to send a command to the board.
    #[error("failed to send data to the board")]
    SendFailed,
}

/// Errors used by the [storage worker](crate::workers::storager).
#[derive(thiserror::Error, Debug, Clone)]
pub enum StorageWorkerError {
    /// The acquisition the storager was set to could not be written to.
    #[error("invalid path provided")]
    InvalidPath,
}

/// Enum for wrapping different types of worker errors into one datatype.
#[derive(thiserror::Error, Debug, Clone)]
pub enum WorkerError {
    /// A [connection worker](crate::workers::connection) error.
    #[error("error in connection worker")]
    Connection(#[from] ConnectionWorkerError),
    /// A [package worker](crate::workers::packager) error.
    #[error("error in package worker")]
    Package(#[from] PackageWorkerError),
    /// A [storage worker](crate::workers::storager) error.
    #[error("error in storage worker")]
    Storage(#[from] StorageWorkerError),
    /// A [answer worker](crate::workers::answer) error.
    #[error("error in answer worker")]
    Answer(#[from] AnswerWorkerError),
}


/// Errors used when opening or using a [connection](crate::connection).
#[derive(thiserror::Error, Debug, Clone)]
pub enum ConnectionError {
    /// Failed to connect to a device
    #[error("failed to connect")]
    ConnectionFailed,
    /// Could not communicate with the device because the connection was dropped.
    #[error("cannot communicate because the connection was dropped")]
    Disconnected,
    /// Failed to configure the device.
    #[error("failed to configure connection")]
    ConfigurationFailed,
    /// A read/write operation timed out.
    #[error("operation took too long")]
    Timeout,
    /// Could not enumerate the devices connected to the system.
    #[error("failed to list devices")]
    ListingFailed,
    /// Uh oh...
    #[error("some other error")]
    Unknown,
}

#[derive(thiserror::Error, Debug, Clone)]
pub enum ParseError {
    /// Could not parse due to an invalid value
    #[error("could not parse due to invalid value")]
    InvalidValue,
}
