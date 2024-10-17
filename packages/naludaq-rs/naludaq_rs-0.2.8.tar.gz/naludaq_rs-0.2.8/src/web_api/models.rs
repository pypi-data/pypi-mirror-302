//! Contains a ridiculous number of structs used to model
//! data for HTTP requests.
//!
//! Structs deriving [`IntoParams`] may be used as arguments by endpoints.
//! Structs deriving [`ToSchema`] may be used as request/response bodies.

use std::{error::Error, net::SocketAddr, collections::HashMap};

use naluacq::list_acquisitions;
use serde::{Deserialize, Serialize};
use utoipa::{IntoParams, ToSchema};

use crate::{
    connection::{Connection, ConnectionInfo, DeviceListEntry},
    error::ConnectionError,
    types::RawAnswer,
    workers::packager::PackagerConfig,
};

use super::state::ServerState;

/// Parameter model for an acquisition name.
#[derive(Deserialize, Debug, IntoParams)]
pub struct AcquisitionName {
    /// Name of an acquisition
    pub name: String,
}

/// Parameter model for fetching selected acquisition details.
#[derive(Deserialize, Debug, IntoParams)]
pub struct AcquisitionShowParams {
    /// Name of an acquisition
    pub name: String,
    /// Whether to include the acquisition path
    #[serde(skip_serializing_if = "Option::is_none")]
    pub path: Option<usize>,
    /// Whether to include the acquisition metadata
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<usize>,
    /// Whether to include the acquisition length
    #[serde(skip_serializing_if = "Option::is_none")]
    pub len: Option<usize>,
    /// Whether to include the acquisition chunk count
    #[serde(skip_serializing_if = "Option::is_none")]
    pub chunk_count: Option<usize>,
    /// Whether to include the acquisition total size
    #[serde(skip_serializing_if = "Option::is_none")]
    pub total_size: Option<usize>,
}

/// Parameter model the show all endpoint
#[derive(Deserialize, Debug, IntoParams)]
pub struct AcquisitionShowAllParams {
    /// Whether to include the acquisition path
    #[serde(skip_serializing_if = "Option::is_none")]
    pub path: Option<usize>,
    /// Whether to include the acquisition metadata
    #[serde(skip_serializing_if = "Option::is_none")]
    pub metadata: Option<usize>,
    /// Whether to include the acquisition length
    #[serde(skip_serializing_if = "Option::is_none")]
    pub len: Option<usize>,
    /// Whether to include the acquisition chunk count
    #[serde(skip_serializing_if = "Option::is_none")]
    pub chunk_count: Option<usize>,
    /// Whether to include the acquisition total size
    #[serde(skip_serializing_if = "Option::is_none")]
    pub total_size: Option<usize>,
}

/// Schema for acquisition metadata.
#[derive(Deserialize, ToSchema, Debug)]
pub struct AcquisitionMetadata {
    /// Metadata for an acquisition, expected to be YAML-encoded.
    pub metadata: String,
}

/// Schema/parameter model representing a target acquisition.
#[derive(Serialize, Deserialize, Debug, IntoParams, ToSchema)]
pub struct OutputAcquisition {
    /// Name of the acquisition. If `None`, then there is no target.
    pub name: Option<String>,
}

/// Parameter model representing an event location
#[derive(Deserialize, Debug, IntoParams)]
pub struct EventLocator {
    /// Name of the acquisition.
    pub acquisition: String,
    /// Index of the event within the acquisition.
    pub index: usize,
}

/// Parameter model pointing to specific misc data in an acquisition
#[derive(Debug, Clone, Serialize, Deserialize, IntoParams)]
pub struct MiscDataLocator {
    /// Name of the acquisition.
    pub acquisition: String,
    /// Name of the misc data type
    #[serde(rename = "type")]
    pub type_name: String,
}

/// Model for moving acquisitions
#[derive(Debug, Clone, Deserialize, IntoParams)]
pub struct AcquisitionMoveRequest {
    /// Name of the source acquisition
    pub source_name: String,
    /// Name of the destination acquisition
    pub dest_name: String,
}

/// Schema for information regarding an acquisition.
#[derive(Serialize, Debug, Default, ToSchema)]
pub struct AcquisitionDetails {
    pub path: Option<String>,
    pub metadata: Option<String>,
    pub len: Option<usize>,
    pub chunk_count: Option<usize>,
    pub total_size: Option<usize>,
}

/// Schema for information about all acquisitions.
#[derive(Serialize, Debug, Default, ToSchema)]
pub struct AllAcquisitionDetails {
    #[serde(flatten)]
    pub details: HashMap<String, AcquisitionDetails>,
}

/// Schema for listing acquisition names.
#[derive(Serialize, Debug, ToSchema)]
pub struct AcquisitionList {
    /// Names of available acquisitions in the root directory of the server.
    pub acquisitions: Vec<String>,
}

/// Schema for hex-encoded data packages.
///
/// Can be used for commands, answers, and events.
#[derive(Serialize, Deserialize, Debug, ToSchema)]
pub struct DataPackages {
    /// Hex-encoded data packages
    pub packages: Vec<String>,
}

impl DataPackages {
    /// Create a [`DataPackages`] instance from several [`RawAnswer`]s.
    pub fn from_raw(raw: &Vec<RawAnswer>) -> Self {
        Self {
            packages: raw.iter().map(|e| hex::encode(e)).collect(),
        }
    }

    /// Convert the data packages to bytes.
    ///
    /// # Panics
    /// Will panic if the data is not valid hex.
    pub fn to_bytes(&self) -> Vec<Vec<u8>> {
        self.packages
            .iter()
            .map(|e| hex::decode(e).unwrap())
            .collect()
    }
}

/// Parameter model for event/answer stop words.
#[derive(Serialize, Deserialize, Debug, IntoParams)]
pub struct DataFormatConfig {
    /// Board model
    pub model: String,
    /// Hex-encoded stop word for events.
    pub events: String,
    /// Hex-encoded stop word for answers.
    pub answers: String,
}

impl DataFormatConfig {
    /// Parses the stop words to binary.
    ///
    /// # Errors
    /// Returns an error if the stop words are not valid hex.
    pub fn parse(&self) -> Result<PackagerConfig, Box<dyn Error>> {
        let events = hex::decode(&self.events)?;
        let answers = hex::decode(&self.answers)?;
        Ok(PackagerConfig::new(&self.model, events, answers))
    }
}

/// Parameter model for UDP connection details.
#[derive(Deserialize, Debug, IntoParams)]
pub struct UdpConnectionAddress {
    /// Socket address which the board receives data on.
    ///
    /// Must be formatted as `"{HOST}:{PORT}"`.
    pub board: String,
    /// Socket address which the board sends data to.
    ///
    /// Must be formatted as `"{HOST}:{PORT}"`.
    pub receiver: String,
}

impl UdpConnectionAddress {
    /// Parse the addresses to [`SocketAddr`] instances.
    ///
    /// # Errors
    /// Returns an error if the addresses are not valid.
    pub fn parse(self) -> Result<(SocketAddr, SocketAddr), Box<dyn Error>> {
        let board = self.board.parse()?;
        let receiver = self.receiver.parse()?;
        Ok((board, receiver))
    }
}

/// Parameter model for configuring serial connections.
#[derive(Deserialize, Debug, IntoParams)]
pub struct SerialConfiguration {
    /// The serial port. If specified, this will close and reopen the connection.
    pub port: Option<String>,
    /// The baud rate. If provided, this will adjust the baud rate.
    pub baud_rate: Option<u32>,
    /// Whether RTS/CTS flow control is enabled. If provided, this will enable/disable
    /// RTS/CTS flow control.
    ///
    /// This is a `u8` value because `IntoParams` doesn't support `bool`s.
    pub rts_cts: Option<u8>,
    /// Timeout in milliseconds for I/O operations. If provided, this will adjust
    /// the timeout.
    pub timeout_ms: Option<usize>,
}

/// Parameter model for configuring D2XX connections.
#[derive(Deserialize, Debug, ToSchema, IntoParams)]
pub struct D2xxConfiguration {
    /// The serial number. If specified, this will close and reopen the connection.
    pub serial_number: Option<String>,
    /// The baud rate. If provided, this will adjust the baud rate.
    pub baud_rate: Option<u32>,
    /// Whether RTS/CTS flow control is enabled. If provided, this will enable/disable
    /// RTS/CTS flow control.
    ///
    /// This is a `u8` value because `IntoParams` doesn't support `bool`s.
    pub rts_cts: Option<u8>, // params don't support bool :(
    /// Timeout for I/O operations. If provided, this will adjust the timeout.
    pub timeouts: Option<D2xxTimeouts>,
}

/// Parameter model for configuring D3XX connections.
#[derive(Deserialize, Debug, ToSchema, IntoParams)]
pub struct D3xxConfiguration {
    /// The serial number. If specified, this will close and reopen the connection.
    pub serial_number: Option<String>,
    /// Timeout for I/O operations. If provided, this will adjust the timeout.
    pub timeouts: Option<D2xxTimeouts>,
}

/// Schema/parameter model for timeouts for a D2XX connection.
#[derive(Serialize, Deserialize, Debug, ToSchema, IntoParams)]
pub struct D2xxTimeouts {
    /// The read timeout in milliseconds.
    pub read_timeout_ms: usize,
    /// The write timeout in milliseconds.
    pub write_timeout_ms: usize,
}

/// Schema for listing available devices.
#[derive(Serialize, Debug, ToSchema)]
pub struct DeviceList {
    /// Vector of available devices.
    pub devices: Vec<DeviceListEntry>,
}

impl Default for DeviceList {
    /// Defaults to an empty list.
    fn default() -> Self {
        Self {
            devices: Vec::new(),
        }
    }
}

impl DeviceList {
    /// Create a new device list from the given entries
    pub fn new(devices: Vec<DeviceListEntry>) -> Self {
        Self { devices }
    }
}

/// Schema representing information about the current connection.
#[derive(Serialize, Debug, ToSchema)]
pub struct ConnectionInfoResponse {
    /// Indicates whether or not there is an open connection.
    connected: bool,
    /// Indicates the type of connection, if one exists.
    ///
    /// Values are `"udp"`, `"serial"`, and `"d2xx"`.
    connection_type: Option<String>,
    /// Contains the connection information, if one exists.
    connection_info: Option<ConnectionInfo>,
}

impl ConnectionInfoResponse {
    /// Construct a new [`ConnectionInfoResponse`] from a connection.
    pub async fn new(connection: Option<Connection>) -> Result<Self, ConnectionError> {
        Ok(match connection {
            Some(connection) => Self {
                connected: true,
                connection_type: Some(
                    match connection {
                        Connection::Udp(_) => "udp",
                        Connection::Serial(_) => "serial",
                        Connection::D2xx(_) => "d2xx",
                        Connection::D3xx(_) => "d3xx",
                    }
                    .to_string(),
                ),
                connection_info: Some(ConnectionInfo::from(&connection).await?),
            },
            None => Self {
                connected: false,
                connection_type: None,
                connection_info: None,
            },
        })
    }
}

/// Struct holding debug information about the server.
#[derive(Debug, Clone, Serialize, ToSchema)]
pub struct SystemInfo {
    /// System information.
    ///
    /// Includes machine, disk, and network specs.
    pub system: system::SystemInfo,
    /// The total disk usage in bytes.
    ///
    /// This is the sum of the size of all acquisitions
    pub disk_usage: usize,
    /// The working directory of the server.
    pub working_dir: String,
}

impl SystemInfo {
    /// Fetch the current system information.
    pub async fn current(state: ServerState) -> Self {
        let disk_usage = list_acquisitions(state.root())
            .into_iter()
            .map(|acq| acq.total_size().unwrap_or(0))
            .sum();
        Self {
            system: system::SystemInfo::current(),
            working_dir: state.root().to_string_lossy().to_string(),
            disk_usage,
        }
    }
}
