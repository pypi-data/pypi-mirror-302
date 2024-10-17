//! Module containing endpoints for reading from/writing to the board.

use axum::{extract::State, Json};
// use hyper::StatusCode;

use super::errors::{RequestError, Result};
use super::{models::DataPackages, state::ServerState};
use crate::error::AnswerWorkerError;
use crate::{
    error::{ConnectionWorkerError, WorkerError},
    types::RawAnswer,
};

/// Send non-read command(s) to the board.
///
/// Sends one or more commands which are not "read" commands.
/// This will write the commands to the board as quickly as possible,
/// in the same order that the commands are given.
///
/// Sending a "read" command using this method is discouraged, since it
/// may misalign the responses for true read commands for the ASIC since
/// they do not support command IDs.
#[utoipa::path(
    put,
    path = "/board/raw",
    request_body=DataPackages,
    responses(
        (status = 200, description = "Data written successfully"),
        (status = 409, description = "No board connection"),
        (status = 500, description = "Server failed to write data")
    ),
)]
#[tracing::instrument(err)]
pub async fn write(
    State(state): State<ServerState>,
    Json(payload): Json<DataPackages>,
) -> Result<Json<()>> {
    match state
        .workers()
        .send_write_commands(payload.to_bytes())
        .await
    {
        Ok(()) => Ok(Json(())),
        Err(WorkerError::Connection(ConnectionWorkerError::NoConnection)) => {
            Err(RequestError::NoConnection)
        }
        Err(e) => {
            tracing::error!("Failed to write data to board: {:?}", e);
            Err(RequestError::Unknown)
        },
    }
}

/// Read register(s) on the board
///
/// Sends one or more "read" commands to the board, awaits the responses,
/// and returns them as part of the response. If successful, the responses
/// are guaranteed to be in the same order as the corresponding commands.
///
/// The commands and answers are both hex strings.
#[utoipa::path(
    get,
    path = "/board/raw",
    request_body=DataPackages,
    responses(
        (status = 200, description = "Read data successfully", body = DataPackages),
        (status = 408, description = "Board did not send a response in time"),
        (status = 409, description = "No board connection"),
        (status = 500, description = "Server failed to read data")
    ),
)]
#[tracing::instrument(err, skip(state))]
pub async fn read(
    State(state): State<ServerState>,
    Json(payload): Json<DataPackages>,
) -> Result<Json<DataPackages>> {
    let commands = payload.to_bytes();
    let connection = state
        .workers()
        .connection_worker()
        .connection()
        .await
        .ok_or(RequestError::NoConnection)?;
    let answers = state
        .workers()
        .answer_worker()
        .read_all(&connection, commands)
        .await
        .into_iter()
        .collect::<core::result::Result<Vec<RawAnswer>, _>>();
    match answers {
        Ok(answers) => Ok(Json(DataPackages::from_raw(&answers))),
        Err(AnswerWorkerError::ReceiveTimeout) => Err(RequestError::TimedOut),
        Err(_) => Err(RequestError::Unknown),
    }
}
