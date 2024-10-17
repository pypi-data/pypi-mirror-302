use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

pub type Result<T, E = RequestError> = core::result::Result<T, E>;

#[derive(thiserror::Error, Debug, Serialize, Deserialize, ToSchema)]
pub enum RequestError {
    #[error("unknown error occurred")]
    Unknown,
    #[error("invalid arguments")]
    InvalidArguments,

    // Connection
    #[error("invalid connection type")]
    InvalidConnectionType,
    #[error("failed to configure connection")]
    ConnectionConfigurationFailed,
    #[error("there is no connection")]
    NoConnection,
    #[error("failed to open a connection")]
    ConnectionFailed,
    #[error("failed to disconnect")]
    DisconnectFailed,

    // Acquisition
    #[error("already exists")]
    AlreadyExists,
    #[error("acquisition name is invalid")]
    InvalidAcquisitionName,
    #[error("no acquisition with the given name")]
    NoSuchAcquisition,
    #[error("event index out of bounds")]
    EventIndexOutOfBounds,
    #[error("event could not be read")]
    EventAccessFailed,

    // Other
    #[error("workers were not started")]
    WorkersNotStarted,
    #[error("timed out while waiting for a response")]
    TimedOut,
}

impl RequestError {
    pub fn status_code(&self) -> StatusCode {
        match self {
            RequestError::NoConnection => StatusCode::CONFLICT,
            RequestError::InvalidConnectionType => StatusCode::CONFLICT,
            RequestError::ConnectionFailed => StatusCode::BAD_REQUEST,
            RequestError::ConnectionConfigurationFailed => StatusCode::INTERNAL_SERVER_ERROR,
            RequestError::TimedOut => StatusCode::REQUEST_TIMEOUT,
            RequestError::AlreadyExists => StatusCode::BAD_REQUEST,
            RequestError::InvalidAcquisitionName => StatusCode::BAD_REQUEST,
            RequestError::NoSuchAcquisition => StatusCode::BAD_REQUEST,
            RequestError::EventIndexOutOfBounds => StatusCode::BAD_REQUEST,
            RequestError::EventAccessFailed => StatusCode::INTERNAL_SERVER_ERROR,
            RequestError::Unknown => StatusCode::INTERNAL_SERVER_ERROR,
            RequestError::InvalidArguments => StatusCode::BAD_REQUEST,
            RequestError::DisconnectFailed => StatusCode::INTERNAL_SERVER_ERROR,
            RequestError::WorkersNotStarted => StatusCode::PRECONDITION_FAILED,
        }
    }
}

impl IntoResponse for RequestError {
    fn into_response(self) -> axum::response::Response {
        let status_code = self.status_code();
        let json = Json(ErrorResponse {
            message: self.to_string(),
            error_id: self as usize,
        });
        (status_code, json).into_response()
    }
}

#[derive(Clone, Debug, Serialize, Deserialize, ToSchema)]
struct ErrorResponse {
    error_id: usize,
    message: String,
}
