//! Module containing endpoints for configuring the server.

use axum::extract::{Query, State};
use axum::Json;
// use hyper::StatusCode;

use super::errors::RequestError;
use super::{models::{SystemInfo, DataFormatConfig}, state::ServerState};

type Result<T> = std::result::Result<T, RequestError>;

/// and answers from the data stream.
///
/// Setting the stop words will also (re)start the packager.
#[utoipa::path(
    put,
    path = "/server/data-format",
    params(DataFormatConfig),
    responses(
        (status = 200, description = "Set stop words successfully"),
        (status = 400, description = "Stop words were not valid hex"),
    ),
)]
#[tracing::instrument(err)]
pub async fn set_packager_configuration(
    State(state): State<ServerState>,
    Query(payload): Query<DataFormatConfig>,
) -> Result<Json<()>> {
    let config = payload.parse().or(Err(RequestError::InvalidArguments))?;
    state
        .workers()
        .package_worker()
        .set_configuration(config)
        .await;
    Ok(Json(()))
}

/// Shut down the server.
#[utoipa::path(
    put,
    path = "/server/shutdown",
    // responses(
    //     (status = 200, description = "Server was shut down successfully"),
    // ),
)]
#[tracing::instrument]
pub async fn shutdown(State(state): State<ServerState>) {
    tracing::info!("Shutting down server...");
    state.workers().stop().await;
}

/// Get debug information
#[utoipa::path(
    put,
    path = "/server/debug-info",
    responses(
        (
            status = 200,
            description = "Successfully retrieved system info",
            body = DebugInfo
        ),
        (status = 500, description = "Failed to retrieve system info"),
    ),
)]
#[tracing::instrument(err)]
pub async fn debug_info(State(state): State<ServerState>) -> Result<Json<SystemInfo>> {
    // generating debug info is pretty I/O-intensive, best to spawn a blocking task
    // to avoid gumming up the server
    let info = tokio::task::spawn_blocking(move || {
        tokio::runtime::Runtime::new()
            .unwrap()
            .block_on(SystemInfo::current(state))
    })
    .await
    .or(Err(RequestError::Unknown))?;
    Ok(Json(info))
}
