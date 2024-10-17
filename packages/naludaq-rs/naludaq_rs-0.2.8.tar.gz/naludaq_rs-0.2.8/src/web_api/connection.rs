//! Module containing endpoints for controlling and querying the connection.

use std::time::Duration;

use axum::{
    extract::{Query, State},
    Json,
};
// use hyper::StatusCode;

use crate::connection::{list_devices, Connection, DeviceListEntry};

use super::{
    errors::{RequestError, Result},
    models::{
        ConnectionInfoResponse, D2xxConfiguration, D3xxConfiguration, DeviceList,
        SerialConfiguration, UdpConnectionAddress,
    },
    state::ServerState,
};

/// Connect to a board over UDP.
///
/// This will disconnect any open connection before attempting to connect.
#[utoipa::path(
    put,
    path = "/connection/udp",
    params(UdpConnectionAddress),
    responses(
        (status = 200, description = "Successfully connected"),
        (status = 400, description = "Connection could not be established due to invalid addresses"),
    ),
)]
#[tracing::instrument(err)]
pub async fn connect_udp(
    State(state): State<ServerState>,
    Query(payload): Query<UdpConnectionAddress>,
) -> Result<Json<()>> {
    let (board, receiver) = payload.parse().or(Err(RequestError::InvalidArguments))?;

    state
        .workers()
        .connection_worker()
        .connect_udp(board, receiver)
        .await
        .or(Err(RequestError::ConnectionFailed))?;
    Ok(Json(()))
}

/// Connect to a board over a serial port.
///
/// This method can also be used to configure an open connection, as long
/// as the "port" field is not provided.
///
/// If connecting, this method will disconnect any open connection before
/// attempting to connect.
///
#[utoipa::path(
    put,
    path = "/connection/serial",
    params(SerialConfiguration),
    responses(
        (status = 200, description = "Successfully connected"),
        (status = 400, description = "Connection could not be established"),
        (status = 409, description = "Attempted to reconfigure a non-existent connection"),
    ),
)]
#[tracing::instrument(err)]
pub async fn configure_serial(
    State(state): State<ServerState>,
    Query(payload): Query<SerialConfiguration>,
) -> Result<Json<()>> {
    let baud_rate = payload.baud_rate.or(Some(115200)).unwrap();
    let worker = state.workers().connection_worker();

    // open connection
    if let Some(ref port) = payload.port {
        worker
            .connect_serial(&port, baud_rate)
            .await
            .or(Err(RequestError::ConnectionFailed))?;
    }

    let connection = match state.workers().connection_worker().connection().await {
        Some(Connection::Serial(conn)) => conn,
        Some(_) => Err(RequestError::InvalidConnectionType)?,
        None => Err(RequestError::InvalidConnectionType)?,
    };

    // No need to set baud rate if it was set when connecting
    if payload.baud_rate.is_some() && payload.port.is_none() {
        connection
            .set_baud_rate(payload.baud_rate.unwrap())
            .await
            .or(Err(RequestError::ConnectionConfigurationFailed))?;
    }

    if let Some(timeout) = payload.timeout_ms {
        connection
            .set_timeout(Duration::from_millis(timeout as _))
            .await
            .or(Err(RequestError::ConnectionConfigurationFailed))?;
    }
    if let Some(rts_cts) = payload.rts_cts {
        let rts_cts = rts_cts == 1;
        connection
            .set_flow_control_rts_cts(rts_cts)
            .await
            .or(Err(RequestError::ConnectionConfigurationFailed))?;
    }
    Ok(Json(()))
}

/// Connect to a board through D2XX.
///
/// This method can also be used to configure an open connection, as long
/// as the "serial_number" field is not provided.
///
/// If connecting, this method will disconnect any open connection before
/// attempting to connect.
///
#[utoipa::path(
    put,
    path = "/connection/d2xx",
    params(D2xxConfiguration),
    responses(
        (status = 200, description = "Successfully connected"),
        (status = 400, description = "Connection could not be established"),
        (status = 409, description = "Attempted to reconfigure a non-existent connection"),
    ),
)]
#[tracing::instrument(err)]
pub async fn configure_d2xx(
    State(state): State<ServerState>,
    Query(payload): Query<D2xxConfiguration>,
) -> Result<Json<()>> {
    let baud_rate = payload.baud_rate.unwrap_or(115200);
    let worker = state.workers().connection_worker();

    // open connection
    if let Some(ref serial_number) = payload.serial_number {
        worker
            .connect_d2xx(&serial_number, baud_rate)
            .await
            .or(Err(RequestError::ConnectionFailed))?;
    }

    let mut connection = match worker.connection().await {
        Some(Connection::D2xx(conn)) => conn,
        Some(_) => Err(RequestError::InvalidConnectionType)?,
        _ => Err(RequestError::NoConnection)?,
    };

    // No need to set baud rate if it was set when connecting
    if payload.baud_rate.is_some() && payload.serial_number.is_none() {
        connection
            .set_baud_rate(payload.baud_rate.unwrap())
            .await
            .or(Err(RequestError::ConnectionConfigurationFailed))?;
    }

    if let Some(timeouts) = payload.timeouts {
        connection
            .set_timeouts(
                Duration::from_millis(timeouts.read_timeout_ms as _),
                Duration::from_millis(timeouts.write_timeout_ms as _),
            )
            .await
            .or(Err(RequestError::ConnectionConfigurationFailed))?;
    }
    if let Some(rts_cts) = payload.rts_cts {
        let rts_cts = rts_cts == 1;
        connection
            .set_flow_control_rts_cts(rts_cts)
            .await
            .or(Err(RequestError::ConnectionConfigurationFailed))?;
    }

    Ok(Json(()))
}

/// Connect to a board through D2XX.
///
/// This method can also be used to configure an open connection, as long
/// as the "serial_number" field is not provided.
///
/// If connecting, this method will disconnect any open connection before
/// attempting to connect.
///
#[utoipa::path(
    put,
    path = "/connection/d3xx",
    params(D3xxConfiguration),
    responses(
        (status = 200, description = "Successfully connected"),
        (status = 400, description = "Connection could not be established"),
        (status = 409, description = "Attempted to reconfigure a non-existent connection"),
    ),
)]
#[tracing::instrument(err)]
pub async fn connect_d3xx(
    State(state): State<ServerState>,
    Query(payload): Query<D3xxConfiguration>,
) -> Result<Json<()>> {
    let worker = state.workers().connection_worker();

    // open connection
    if let Some(ref serial_number) = payload.serial_number {
        worker
            .connect_d3xx(&serial_number)
            .await
            .or(Err(RequestError::ConnectionFailed))?;
    }

    let mut connection = match worker.connection().await {
        Some(Connection::D3xx(conn)) => conn,
        Some(_) => Err(RequestError::InvalidConnectionType)?,
        _ => Err(RequestError::NoConnection)?,
    };

    if let Some(timeouts) = payload.timeouts {
        connection
            .set_timeouts(
                Duration::from_millis(timeouts.read_timeout_ms as u64),
                Duration::from_millis(timeouts.write_timeout_ms as u64),
            )
            .await
            .or(Err(RequestError::ConnectionConfigurationFailed))?;
    }

    Ok(Json(()))
}

/// Disconnect any open connection.
#[utoipa::path(
    put,
    path = "/connection/disconnect",
    responses(
        (status = 200, description = "Successfully disconnected"),
        (status = 500, description = "Server failed to disconnect"),
    ),
)]
#[tracing::instrument(err)]
pub async fn disconnect(State(state): State<ServerState>) -> Result<Json<()>> {
    state
        .workers()
        .connection_worker()
        .disconnect()
        .await
        .or(Err(RequestError::DisconnectFailed))?;
    Ok(Json(()))
}

/// Clear input and output buffers for the current connection.
#[utoipa::path(
    put,
    path = "/connection/clear",
    responses(
        (status = 200, description = "Successfully cleared buffers"),
        (status = 409, description = "There is no connection"),
        (status = 500, description = "Server failed to clear buffers"),
    ),
)]
#[tracing::instrument(err)]
pub async fn clear_buffers(State(state): State<ServerState>) -> Result<Json<()>> {
    let connection = state
        .workers()
        .connection_worker()
        .connection()
        .await
        .ok_or(RequestError::NoConnection)?;
    match connection {
        Connection::Serial(serial) => serial
            .clear_buffers()
            .await
            .or(Err(RequestError::Unknown))?,
        Connection::D2xx(d2xx) => d2xx.clear_buffers().await.or(Err(RequestError::Unknown))?,
        _ => (),
    }
    state.workers().answer_worker().reset().await;
    state
        .workers()
        .package_worker()
        .reset()
        .await
        .or(Err(RequestError::WorkersNotStarted))?;
    Ok(Json(()))
}

/// Get information about the current connection.
#[utoipa::path(
    get,
    path = "/connection/info",
    responses(
        (status = 200, description = "Successfully fetched connection details", body = ConnectionInfoResponse),
        (status = 500, description = "Server failed to fetch connection details"),
    ),
)]
#[tracing::instrument(err)]
pub async fn connection_info(
    State(state): State<ServerState>,
) -> Result<Json<ConnectionInfoResponse>> {
    let connection = state.workers().connection_worker().connection().await;
    Ok(Json(
        ConnectionInfoResponse::new(connection)
            .await
            .or(Err(RequestError::Unknown))?,
    ))
}

/// List all devices connected to the system.
///
/// Includes the currently device, if connected.
#[utoipa::path(
    get,
    path = "/connection/list",
    responses(
        (status = 200, description = "Successfully listed devices", body = DeviceList),
        (status = 500, description = "Server failed to list devices"),
    ),
)]
#[tracing::instrument(err)]
pub async fn list_connections(State(state): State<ServerState>) -> Result<Json<DeviceList>> {
    let mut devices = list_devices().or(Err(RequestError::Unknown))?;

    // add current connection to the list, since it doesn't get enumerated
    if let Some(conn) = state.workers().connection_worker().connection().await {
        if let Some(dev) = DeviceListEntry::from_connection(&conn).await {
            devices.push(dev)
        }
    }

    Ok(Json(DeviceList::new(devices)))
}
