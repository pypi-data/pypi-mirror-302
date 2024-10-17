//! Module containing utilities for connecting to a device.
//!
//! The following connection types are supported:
//! - [UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol)
//! - [D2XX](https://www.ftdichip.com/Support/Documents/ProgramGuides/D2XX_Programmer's_Guide(FT_000071).pdf)
//! - [D3XX](https://ftdichip.com/wp-content/uploads/2020/07/AN_379-D3xx-Programmers-Guide-1.pdf)
//! - [Serial UART](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter)
//!
//! The [`Connection`] enum is a wrapper over the inner connection type, and may be safely cloned and
//! passed between threads.

use std::{
    sync::{
        atomic::{AtomicBool, AtomicU32, Ordering},
        Arc,
    },
    time::Duration,
};

use ft60x_rs::D3xxError;
use libftd2xx::{FtdiCommon, Parity};
use serde::{Deserialize, Serialize};
use tokio::{net::UdpSocket, sync::Mutex};
use tokio_serial::{SerialPort, SerialPortBuilderExt, SerialStream};
use utoipa::ToSchema;

use crate::{
    constants::{
        D2XX_READ_TIMEOUT, D2XX_WRITE_TIMEOUT, D3XX_CONNECTION_ATTEMPT_DELAY, D3XX_READ_TIMEOUT,
        D3XX_WRITE_TIMEOUT, SERIAL_TIMEOUT,
    },
    error::ConnectionError,
};

/// Wrapper enum containing a connection of one of the supported types.
///
/// A `Connection` may be cloned and passed between threads safely.
///
/// Note: The API for each of the connection types varies slightly.
///
/// # Examples
/// ```ignore
/// let serial = SerialConnection::new("COM5", 115_200).expect("connection failed");
/// let conn = Connection::Serial(serial);
/// println!("Connection: {:?}", conn);
/// ```
#[derive(Clone, Debug)]
pub enum Connection {
    Udp(Arc<UdpSocket>),
    Serial(SerialConnection),
    D2xx(D2xxConnection),
    D3xx(D3xxConnection),
}

impl Connection {
    /// Send data to the board.
    pub async fn send(&self, buf: &[u8]) -> Result<usize, ConnectionError> {
        match self {
            Connection::Udp(udp) => udp.send(buf).await.ok(),
            Connection::Serial(serial) => serial.send(buf).await.ok(),
            Connection::D2xx(d2xx) => d2xx.send(buf).await.ok(),
            Connection::D3xx(d2xx) => d2xx.send(buf).await.ok(),
        }
        .ok_or(ConnectionError::Unknown)
    }
}

/// Wrapper enum containing information about a connection.
#[derive(Serialize, Deserialize, Debug, Clone, ToSchema)]
#[serde(untagged)]
pub enum ConnectionInfo {
    Udp(UdpConnectionInfo),
    Serial(SerialConnectionInfo),
    D2xx(D2xxConnectionInfo),
    D3xx(D3xxConnectionInfo),
}

impl ConnectionInfo {
    /// Extracts connection info from an existing connection.
    ///
    /// # Errors
    /// A [`ConnectionError`] will be returned if any aspect of the connection cannot be determined.
    ///
    /// # Examples
    /// ```ignore
    /// let serial = SerialConnection::new("COM5", 115_200).expect("connection failed");
    /// let conn = Connection::Serial(serial);
    /// let info = ConnectionInfo::from(conn).expect("failed to retrieve connection info");
    /// println!("Connection info: {:?}", info);
    /// ```
    pub async fn from(connection: &Connection) -> Result<Self, ConnectionError> {
        Ok(match connection {
            Connection::Udp(ref udp) => Self::Udp(UdpConnectionInfo::new(udp)?),
            Connection::Serial(ref serial) => Self::Serial(serial.info()),
            Connection::D2xx(ref d2xx) => Self::D2xx(d2xx.info().await?),
            Connection::D3xx(ref d3xx) => Self::D3xx(d3xx.info().await?),
        })
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub enum DeviceListEntry {
    /// Represents a serial device.
    Serial { port: String },
    /// Represents a D2XX device.
    D2xx {
        serial_number: String,
        com_port: Option<u32>,
        index: usize,
        description: String,
    },
    /// Represents a D3XX device.
    D3xx {
        serial_number: String,
        description: String,
    },
}

impl DeviceListEntry {
    /// Construct a [`DeviceListEntry`] from an open connection.
    ///
    /// If not all information could be retrieved, or the connection
    /// type is not valid, `None` is returned.
    pub async fn from_connection(conn: &Connection) -> Option<DeviceListEntry> {
        match conn {
            Connection::D2xx(conn) => Self::from_d2xx(conn).await,
            Connection::Serial(conn) => Self::from_serial(conn),
            _ => None,
        }
    }

    /// Construct a [`DeviceListEntry`] from an open D2XX connection.
    ///
    /// If not all information could be retrieved, `None` is returned.
    pub async fn from_d2xx(conn: &D2xxConnection) -> Option<DeviceListEntry> {
        Some(DeviceListEntry::D2xx {
            serial_number: conn.serial_number().to_string(),
            com_port: conn.com_port().await.unwrap_or(None),
            index: 0,
            description: conn.description().await.ok()?,
        })
    }

    /// Construct a [`DeviceListEntry`] from an open serial connection
    ///
    /// If not all information could be retrieved, `None` is returned.
    pub fn from_serial(conn: &SerialConnection) -> Option<DeviceListEntry> {
        Some(DeviceListEntry::Serial {
            port: conn.port().to_string(),
        })
    }
}

/// List all serial and D2XX devices available to the system.
///
/// This list will not include any devices currently in use.
///
/// # Errors
/// If serial and D2XX devices could no be listed, a [`ConnectionError::ListingFailed`] error is returned.
pub fn list_devices() -> Result<Vec<DeviceListEntry>, ConnectionError> {
    let serial_devices_res = list_serial_devices().or(Err(ConnectionError::ListingFailed));
    let d2xx_devices_res = list_d2xx_devices().or(Err(ConnectionError::ListingFailed));
    let d3xx_devices_res = list_d3xx_devices().or(Err(ConnectionError::ListingFailed));
    if serial_devices_res.is_err() && d2xx_devices_res.is_err() && d3xx_devices_res.is_err() {
        return Err(ConnectionError::ListingFailed);
    }

    let mut devices = Vec::new();
    if let Ok(devs) = serial_devices_res {
        devices.extend(devs);
    }
    if let Ok(devs) = d2xx_devices_res {
        devices.extend(devs);
    }
    if let Ok(devs) = d3xx_devices_res {
        devices.extend(devs);
    }
    Ok(devices)
}

// ====================================================================================================

/// A connection to a board through [serial UART](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter).
///
/// This struct may be cloned and is thread-safe.
#[derive(Clone, Debug)]
pub struct SerialConnection {
    /// Mutex holding the inner serial stream. This allows the serial connection
    /// to be passed between threads and accessed "asynchronously".
    inner: Arc<Mutex<SerialStream>>,
    /// Name of the port.
    ///
    /// On Windows this is a COM port name, while on Linux it is the path to the
    /// device (e.g. `"/dev/ttyUSB0"`)
    port: String,
    /// The baud rate for the connection.
    ///
    /// This is stored as an atomic type to avoid wrapping the value in a mutex.
    baud_rate: Arc<AtomicU32>,
    /// Whether RTS/CTS flow control is enabled.
    ///
    /// This is stored as an atomic type to avoid wrapping the value in a mutex.
    rts_cts_enabled: Arc<AtomicBool>,
}

impl SerialConnection {
    /// Attempts to open a new connection to a serial device.
    ///
    /// On Windows the port is a COM port name, while on Linux it is the path to the
    /// device (e.g. `"/dev/ttyUSB0"`).
    ///
    /// Flow control will be disabled by default when opening the device.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the connection could not be opened or configured.
    ///
    /// # Examples
    /// ```ignore
    /// let serial = Serial::new("COM5", 115_200).expect("connection failed");
    /// ```
    #[tracing::instrument(err)]
    pub async fn new(port: String, baud_rate: u32) -> Result<Self, ConnectionError> {
        tracing::info!("Attempting to connect serial device");
        let stream = tokio_serial::new(port.clone(), baud_rate)
            .timeout(SERIAL_TIMEOUT)
            .open_native_async()
            .or(Err(ConnectionError::ConnectionFailed))?;

        let conn = Self {
            inner: Arc::new(Mutex::new(stream)),
            port,
            baud_rate: Arc::new(AtomicU32::new(baud_rate)),
            rts_cts_enabled: Arc::new(AtomicBool::new(false)),
        };
        conn.set_flow_control_rts_cts(false).await?;
        Ok(conn)
    }

    /// Retrieves information about this connection.
    pub fn info(&self) -> SerialConnectionInfo {
        SerialConnectionInfo {
            port: self.port().into(),
            baud_rate: self.baud_rate(),
            rts_cts: self.flow_control_rtscts(),
        }
    }

    /// Returns the port the connection was opened on.
    pub fn port(&self) -> &str {
        &self.port
    }

    /// Returns the last baud rate the connection was set to.
    pub fn baud_rate(&self) -> u32 {
        self.baud_rate.load(Ordering::Relaxed)
    }

    /// Attempts to set the baud rate.
    ///
    /// # Errors
    /// A [`ConnectionError::ConfigurationFailed`] error is returned if the baud
    /// rate could not be set.
    #[tracing::instrument(skip(self), err)]
    pub async fn set_baud_rate(&self, baud_rate: u32) -> Result<(), ConnectionError> {
        tracing::info!("Setting baud rate");
        let mut guard = self.inner.lock().await;
        guard
            .set_baud_rate(baud_rate)
            .or(Err(ConnectionError::ConfigurationFailed))?;
        self.baud_rate.store(baud_rate, Ordering::Relaxed);
        Ok(())
    }

    /// Returns the last I/O timeout set for the device.
    pub async fn timeout(&self) -> Duration {
        let guard = self.inner.lock().await;
        guard.timeout()
    }

    /// Attempts to set the timeout for I/O.
    ///
    /// # Errors
    /// A [`ConnectionError::ConfigurationFailed`] error is returned if the timeout
    /// could not be set.
    #[tracing::instrument(skip(self), err)]
    pub async fn set_timeout(&self, timeout: Duration) -> Result<(), ConnectionError> {
        let mut guard = self.inner.lock().await;
        guard
            .set_timeout(timeout)
            .or(Err(ConnectionError::ConfigurationFailed))
    }

    /// Get whether flow control is set to RTS/CTS
    pub fn flow_control_rtscts(&self) -> bool {
        self.rts_cts_enabled.load(Ordering::Relaxed)
    }

    /// Attempts to enable or disable RTS/CTS flow control.
    ///
    /// # Errors
    /// A [`ConnectionError::ConfigurationFailed`] error is returned if the flow
    /// control could not be changed.
    #[tracing::instrument(skip(self), err)]
    pub async fn set_flow_control_rts_cts(&self, enabled: bool) -> Result<(), ConnectionError> {
        tracing::debug!("Setting flow control (RTS/CTS) to {enabled}");
        let mut guard = self.inner.lock().await;
        guard
            .set_flow_control(match enabled {
                true => tokio_serial::FlowControl::Hardware,
                false => tokio_serial::FlowControl::None,
            })
            .or(Err(ConnectionError::ConfigurationFailed))?;
        self.rts_cts_enabled.store(enabled, Ordering::Relaxed);
        Ok(())
    }

    /// Clears the input and output buffers.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the buffers could not be cleared.
    pub async fn clear_buffers(&self) -> Result<(), ConnectionError> {
        self.clear_input_buffer().await?;
        self.clear_output_buffer().await
    }

    /// Clear the input buffer. Any discarded data will not be received.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the buffers could not be cleared.
    #[tracing::instrument(skip(self), err)]
    pub async fn clear_input_buffer(&self) -> Result<(), ConnectionError> {
        let guard = self.inner.lock().await;
        guard
            .clear(tokio_serial::ClearBuffer::Input)
            .or(Err(ConnectionError::Unknown))?;
        Ok(())
    }

    /// Clear the output buffer. Discarded data will not be received by the board.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the buffers could not be cleared.
    #[tracing::instrument(skip(self), err)]
    pub async fn clear_output_buffer(&self) -> Result<(), ConnectionError> {
        let guard = self.inner.lock().await;
        guard
            .clear(tokio_serial::ClearBuffer::Output)
            .or(Err(ConnectionError::Unknown))?;
        Ok(())
    }

    /// Attempts to send binary data to the board.
    ///
    /// On success the number of bytes written is returned.
    ///
    /// # Errors
    /// A [`ConnectionError::Timeout`] error is returned if the data could not be
    /// written in time.
    pub async fn send(&self, buf: &[u8]) -> Result<usize, ConnectionError> {
        let mut guard = self.inner.lock().await;
        guard.try_write(buf).or(Err(ConnectionError::Timeout))
    }

    /// Attempts to receive some number of bytes from the board into a buffer.
    ///
    /// On success the number of bytes written is returned.
    ///
    /// # Errors
    /// A [`ConnectionError::Timeout`] error is returned if the data could not be read.
    pub async fn recv(&self, buf: &mut [u8]) -> Result<usize, ConnectionError> {
        let mut guard = self.inner.lock().await;
        guard.try_read(buf).or(Err(ConnectionError::Timeout))
    }
}

/// Holds information about a serial connection.
///
/// # Examples
/// ```ignore
/// let serial = Serial::new("COM5", 115_200).expect("connection failed");
/// let info = serial.info();
/// println!("Info: {:?}", info);
/// ```
#[derive(Serialize, Deserialize, Debug, Clone, ToSchema)]
pub struct SerialConnectionInfo {
    /// The serial port.
    pub port: String,
    /// Baud rate of the connection.
    pub baud_rate: u32,
    /// Whether flow control is set to RTS/CTS.
    pub rts_cts: bool,
}

/// Get a list of serial devices connected to the system.
///
/// This list will not include any devices currently in use.
///
/// # Errors
/// Returns a [`ConnectionError::ListingFailed`] error if the serial devices could not
/// be enumerated.
#[tracing::instrument(err)]
pub fn list_serial_devices() -> Result<Vec<DeviceListEntry>, ConnectionError> {
    Ok(tokio_serial::available_ports()
        .or(Err(ConnectionError::ListingFailed))?
        .iter()
        .map(|e| DeviceListEntry::Serial {
            port: e.port_name.clone(),
        })
        .collect())
}

// ====================================================================================================
/// A connection to a board through [D2XX](https://www.ftdichip.com/Support/Documents/ProgramGuides/D2XX_Programmer's_Guide(FT_000071).pdf).
///
/// This struct may be cloned and is thread-safe.
#[derive(Clone, Debug)]
pub struct D2xxConnection {
    /// Mutex holding the inner d2xx handle. This allows the connection
    /// to be passed between threads and accessed "asynchronously".
    inner: Arc<Mutex<libftd2xx::Ftdi>>,
    /// Serial number used when opening the device.
    serial_number: String,
    /// The baud rate for the connection.
    ///
    /// This is stored as an atomic type to avoid wrapping the value in a mutex.
    baud_rate: Arc<AtomicU32>,
    /// Whether RTS/CTS flow control is enabled.
    ///
    /// This is stored as an atomic type to avoid wrapping the value in a mutex.
    rts_cts_enabled: Arc<AtomicBool>,
}

impl D2xxConnection {
    /// Attempts to open a new connection to a D2XX device.
    ///
    /// A couple of configurations are set when opening the device:
    /// - Flow control will be disabled.
    /// - Data characterstics will be set to 8 bits per word, 1 stop bit, and no parity.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the connection could not be opened or configured.
    ///
    /// # Examples
    /// ```ignore
    /// let d2xx = D2xx::new("SERIAL_NUMBER", 115_200).expect("connection failed");
    /// ```
    #[tracing::instrument(err)]
    pub async fn new(serial: &str, baud_rate: u32) -> Result<Self, ConnectionError> {
        tracing::info!("Attempting to connect D2XX device");
        let mut conn = libftd2xx::Ftdi::with_serial_number(serial)
            .or(Err(ConnectionError::ConnectionFailed))?;
        conn.set_data_characteristics(
            libftd2xx::BitsPerWord::Bits8,
            libftd2xx::StopBits::Bits1,
            Parity::No,
        )
        .or(Err(ConnectionError::ConfigurationFailed))?;
        let mut conn = D2xxConnection {
            inner: Arc::new(Mutex::new(conn)),
            serial_number: serial.into(),
            baud_rate: Arc::new(AtomicU32::new(baud_rate)),
            rts_cts_enabled: Arc::new(AtomicBool::new(false)),
        };
        conn.set_baud_rate(baud_rate).await?;
        conn.set_timeouts(D2XX_READ_TIMEOUT.clone(), D2XX_WRITE_TIMEOUT.clone())
            .await?;
        conn.set_flow_control_rts_cts(false).await?;
        Ok(conn)
    }

    /// Retrieves information about this connection.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if one or more connection details could not
    /// be retrieved.
    #[tracing::instrument(skip(self), err)]
    pub async fn info(&self) -> Result<D2xxConnectionInfo, ConnectionError> {
        Ok(D2xxConnectionInfo {
            serial_number: self.serial_number().into(),
            com_port: self.com_port().await.unwrap_or_default(),
            baud_rate: self.baud_rate(),
            rts_cts: self.flow_control_rtscts(),
        })
    }

    /// Get the device serial number
    pub fn serial_number(&self) -> &str {
        &self.serial_number
    }

    /// Get the description of the device
    ///
    /// # Errors
    /// Returns a [`ConnectionError`] if the device information could not be read.
    pub async fn description(&self) -> Result<String, ConnectionError> {
        let mut guard = self.inner.lock().await;
        let info = guard.device_info().or(Err(ConnectionError::Unknown))?;
        Ok(info.description)
    }

    /// Get the corresponding VCP COM port.
    ///
    /// This function is only available on Windows.
    ///
    /// # Errors
    /// This will return a [`ConnectionError`] if the device has no corresponding COM port
    #[cfg(windows)]
    #[tracing::instrument(skip(self), err)]
    pub async fn com_port(&self) -> Result<Option<u32>, ConnectionError> {
        let mut guard = self.inner.lock().await;
        Ok(guard.com_port_number().or(Err(ConnectionError::Unknown))?)
    }

    /// Get the corresponding VCP COM port.
    ///
    /// This will always return an error.
    #[cfg(not(windows))]
    pub async fn com_port(&self) -> Result<Option<u32>, ConnectionError> {
        Err(ConnectionError::Unknown)
    }

    /// Returns the last baud rate the connection was set to.
    pub fn baud_rate(&self) -> u32 {
        self.baud_rate.load(Ordering::Relaxed)
    }

    /// Attempts to set the baud rate.
    ///
    /// # Errors
    /// A [`ConnectionError::ConfigurationFailed`] error is returned if the baud
    /// rate could not be set.
    #[tracing::instrument(skip(self), err)]
    pub async fn set_baud_rate(&mut self, baud_rate: u32) -> Result<(), ConnectionError> {
        tracing::info!("Setting baud rate");
        let mut guard = self.inner.lock().await;
        guard
            .set_baud_rate(baud_rate)
            .or(Err(ConnectionError::ConfigurationFailed))?;
        self.baud_rate.store(baud_rate, Ordering::Relaxed);
        Ok(())
    }

    /// Attempts to set the timeout for I/O.
    ///
    /// # Errors
    /// A [`ConnectionError::ConfigurationFailed`] error is returned if the timeout
    /// could not be set.
    #[tracing::instrument(skip(self), err)]
    pub async fn set_timeouts(
        &mut self,
        read: Duration,
        write: Duration,
    ) -> Result<(), ConnectionError> {
        let mut guard = self.inner.lock().await;
        guard
            .set_timeouts(read, write)
            .or(Err(ConnectionError::ConfigurationFailed))
    }

    /// Get whether flow control is set to RTS/CTS
    pub fn flow_control_rtscts(&self) -> bool {
        self.rts_cts_enabled.load(Ordering::Relaxed)
    }

    /// Attempts to enable or disable RTS/CTS flow control.
    ///
    /// # Errors
    /// A [`ConnectionError::ConfigurationFailed`] error is returned if the flow
    /// control could not be changed.
    #[tracing::instrument(skip(self), err)]
    pub async fn set_flow_control_rts_cts(&self, enabled: bool) -> Result<(), ConnectionError> {
        tracing::debug!("Setting flow control (RTS/CTS) to {enabled}");
        let mut guard = self.inner.lock().await;
        if enabled {
            guard
                .set_flow_control_rts_cts()
                .or(Err(ConnectionError::ConfigurationFailed))?;
        } else {
            guard
                .set_flow_control_none()
                .or(Err(ConnectionError::ConfigurationFailed))?;
        }
        self.rts_cts_enabled.store(enabled, Ordering::Relaxed);
        Ok(())
    }

    /// Clears the input and output buffers.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the buffers could not be cleared.
    pub async fn clear_buffers(&self) -> Result<(), ConnectionError> {
        self.clear_input_buffer().await?;
        self.clear_output_buffer().await
    }

    /// Clear the input buffer. Any discarded data will not be received.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the buffers could not be cleared.
    #[tracing::instrument(skip(self), err)]
    pub async fn clear_input_buffer(&self) -> Result<(), ConnectionError> {
        let mut guard = self.inner.lock().await;
        guard.purge_rx().or(Err(ConnectionError::Unknown))?;
        Ok(())
    }

    /// Clear the output buffer. Discarded data will not be received by the board.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the buffers could not be cleared.
    #[tracing::instrument(skip(self), err)]
    pub async fn clear_output_buffer(&self) -> Result<(), ConnectionError> {
        let mut guard = self.inner.lock().await;
        guard.purge_tx().or(Err(ConnectionError::Unknown))?;
        Ok(())
    }

    /// Attempts to send binary data to the board.
    ///
    /// On success the number of bytes written is returned.
    ///
    /// # Errors
    /// A [`ConnectionError::Timeout`] error is returned if the data could not be
    /// written in time.
    pub async fn send(&self, buf: &[u8]) -> Result<usize, ConnectionError> {
        let mut guard = self.inner.lock().await;
        guard.write(buf).or(Err(ConnectionError::Timeout))
    }

    /// Attempts to receive some number of bytes from the board into a buffer.
    ///
    /// On success the number of bytes written is returned.
    ///
    /// # Errors
    /// A [`ConnectionError::Timeout`] error is returned if the data could not be read.
    pub async fn recv(&self, buf: &mut [u8]) -> Result<usize, ConnectionError> {
        let mut guard = self.inner.lock().await;
        guard.read(buf).or(Err(ConnectionError::Timeout))
    }
}

/// Holds information about a D2XX connection.
///
/// # Examples
/// ```ignore
/// let d2xx = D2xxConnection::new("SERIAL_NUMBER", 115_200).expect("connection failed");
/// let info = d2xx.info().expect("failed to read info");
/// println!("Info: {:?}", info);
/// ```
#[derive(Serialize, Deserialize, Debug, Clone, ToSchema)]
pub struct D2xxConnectionInfo {
    /// Serial number of the device.
    pub serial_number: String,
    /// Corresponding COM port if available.
    pub com_port: Option<u32>,
    /// Baud rate of the connection
    pub baud_rate: u32,
    /// Whether flow control is set to RTS/CTS.
    pub rts_cts: bool,
}

/// Get a list of D2XX devices connected to the system.
///
/// This list will not include any devices currently in use.
///
/// # Errors
/// Returns a [`ConnectionError::ListingFailed`] error if the D2XX devices could not
/// be enumerated.
#[tracing::instrument(err)]
pub fn list_d2xx_devices() -> Result<Vec<DeviceListEntry>, ConnectionError> {
    Ok(libftd2xx::list_devices()
        .or(Err(ConnectionError::ListingFailed))?
        .iter()
        .enumerate()
        .filter_map(|(i, e)| {
            if e.serial_number.is_empty() {
                None
            } else {
                Some(DeviceListEntry::D2xx {
                    serial_number: e.serial_number.clone(),
                    com_port: libftd2xx::Ftdi::with_serial_number(&e.serial_number)
                        .and_then(|mut d| Ok(d2xx_com_port(&mut d)))
                        .unwrap_or(None),
                    index: i,
                    description: e.description.clone(),
                })
            }
        })
        .collect())
}

/// Fetch the COM port from a [`libftd2xx::Ftdi`] device.
///
/// Returns `None` on failure or on linux machines.
#[cfg(all(any(windows, doc), not(doctest)))]
fn d2xx_com_port(device: &mut libftd2xx::Ftdi) -> Option<u32> {
    device.com_port_number().unwrap_or(None)
}

/// Fetch the COM port from a [`libftd2xx::Ftdi`] device.
///
/// Returns `None` on failure or on linux machines.
#[cfg(not(all(any(windows, doc), not(doctest))))]
fn d2xx_com_port(device: &mut libftd2xx::Ftdi) -> Option<u32> {
    None
}

// ====================================================================================================

/// A connection to a board through [D3XX](https://ftdichip.com/wp-content/uploads/2020/07/AN_379-D3xx-Programmers-Guide-1.pdf).
///
/// This struct may be cloned and is thread-safe.
#[derive(Clone, Debug)]
pub struct D3xxConnection {
    /// Mutex holding the inner d3xx handle. This allows the connection
    /// to be passed between threads and accessed "asynchronously".
    inner: Arc<Mutex<ft60x_rs::Device>>,
    /// Serial number used when opening the device.
    serial_number: String,
}

impl D3xxConnection {
    /// Attempts to open a new connection to a D3XX device.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the connection could not be opened or configured.
    ///
    /// # Examples
    /// ```ignore
    /// let d3xx = D3xx::new("SERIAL_NUMBER").expect("connection failed");
    /// ```
    #[cfg(windows)]
    #[tracing::instrument(err)]
    pub async fn new(serial: &str) -> Result<Self, ConnectionError> {
        tracing::info!("Attempting to connect D3XX device");
        let conn = ft60x_rs::Device::open_with_serial_number(serial)
            .or(Err(ConnectionError::ConnectionFailed))?;
        let mut conn = Self {
            inner: Arc::new(Mutex::new(conn)),
            serial_number: serial.into(),
        };
        conn.set_timeouts(D3XX_READ_TIMEOUT.clone(), D3XX_WRITE_TIMEOUT.clone())
            .await?;
        Ok(conn)
    }

    /// Attempts to open a new connection to a D3XX device with a timeout.
    ///
    /// This function is useful when possibly attempting to reconnect to the same
    /// device after disconnecting from it, since the D3XX drivers have a cooldown period
    /// during which a device cannot be reconnected to (about 500 ms).
    ///
    /// This function will repeatedly attempt to connect to the device until the timeout
    /// is reached, re-attempting at intervals which increase linearly.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if the connection could not be opened or configured.
    ///
    /// # Examples
    /// ```ignore
    /// let timeout = Duration::from_millis(500);
    /// let d3xx = D3xx::new_with_timeout("SERIAL_NUMBER", &timeout).expect("connection failed");
    /// ```
    #[tracing::instrument(err)]
    pub async fn new_with_timeout(
        serial: &str,
        timeout: &Duration,
    ) -> Result<Self, ConnectionError> {
        // Extra initial attempt so we can report the error later on timeout.
        let err = match Self::new(serial).await {
            Ok(c) => return Ok(c),
            Err(e) => e,
        };
        tokio::time::timeout(timeout.clone(), async move {
            let base_timeout = D3XX_CONNECTION_ATTEMPT_DELAY;
            let mut attempts = 1;

            loop {
                // avoid spamming 🍣 the drivers (linear backoff)
                let timeout = base_timeout * attempts;
                tokio::time::sleep(timeout).await;

                if let Ok(c) = Self::new(serial).await {
                    break c;
                }
                attempts += 1
            }
        })
        .await
        .or(Err(err))
    }

    /// Attempts to open a new connection to a D3XX device.
    ///
    /// Will always return an error on non-windows platforms.
    #[cfg(not(windows))]
    #[tracing::instrument(err)]
    pub async fn new(_serial: &str) -> Result<Self, ConnectionError> {
        tracing::error!("D3XX connections are only supported on Windows");
        Err(ConnectionError::ConnectionFailed)
    }

    /// Retrieves information about this connection.
    ///
    /// # Errors
    /// A [`ConnectionError`] is returned if one or more connection details could not
    /// be retrieved.
    #[tracing::instrument(skip(self), err)]
    pub async fn info(&self) -> Result<D3xxConnectionInfo, ConnectionError> {
        Ok(D3xxConnectionInfo {
            serial_number: self.serial_number().into(),
            description: self.description().await?,
        })
    }

    /// Get the device serial number
    pub fn serial_number(&self) -> &str {
        &self.serial_number
    }

    /// Get the description of the device
    ///
    /// # Errors
    /// Returns a [`ConnectionError`] if the device information could not be read.
    pub async fn description(&self) -> Result<String, ConnectionError> {
        let guard = self.inner.lock().await;
        let info = guard.info().or(Err(ConnectionError::Unknown))?;
        info.description().or(Ok("".to_owned()))
    }

    /// Attempts to set the timeout for I/O.
    ///
    /// # Errors
    /// A [`ConnectionError::ConfigurationFailed`] error is returned if the timeout
    /// could not be set.
    #[tracing::instrument(skip(self), err)]
    pub async fn set_timeouts(
        &mut self,
        read: Duration,
        write: Duration,
    ) -> Result<(), ConnectionError> {
        let guard = self.inner.lock().await;
        guard
            .set_timeout(ft60x_rs::Pipe::Out0, write)
            .or(Err(ConnectionError::ConfigurationFailed))?;
        guard
            .set_timeout(ft60x_rs::Pipe::In0, read)
            .or(Err(ConnectionError::ConfigurationFailed))?;
        Ok(())
    }

    /// Attempts to send binary data to the board.
    ///
    /// On success the number of bytes written is returned.
    ///
    /// # Errors
    /// A [`ConnectionError::Timeout`] error is returned if the data could not be
    /// written in time.
    pub async fn send(&self, buf: &[u8]) -> Result<usize, ConnectionError> {
        let guard = self.inner.lock().await;
        guard
            .write(ft60x_rs::Pipe::Out0, buf)
            .or(Err(ConnectionError::Timeout))
    }

    /// Attempts to receive some number of bytes from the board into a buffer.
    ///
    /// On success the number of bytes written is returned.
    ///
    /// # Errors
    /// A [`ConnectionError::Timeout`] error is returned if the data could not be read.
    pub async fn recv(&self, buf: &mut [u8]) -> Result<usize, ConnectionError> {
        let guard = self.inner.lock().await;
        guard
            .read(ft60x_rs::Pipe::In0, buf)
            .or(Err(ConnectionError::Timeout))
    }
}

/// Holds information about a D3XX connection.
#[derive(Serialize, Deserialize, Debug, Clone, ToSchema)]
pub struct D3xxConnectionInfo {
    /// Serial number of the device.
    pub serial_number: String,
    /// Description of the device.
    pub description: String,
}

/// Get a list of D3XX devices connected to the system.
///
/// This list will not include any devices currently in use.
///
/// # Errors
/// Returns a [`ConnectionError::ListingFailed`] error if the D2XX devices could not
/// be enumerated.
#[tracing::instrument(err)]
pub fn list_d3xx_devices() -> Result<Vec<DeviceListEntry>, ConnectionError> {
    Ok(ft60x_rs::list_devices()
        .or(Err(ConnectionError::ListingFailed))?
        .iter()
        .filter_map(|e| {
            let serial_number = e.serial_number().ok()?;
            let description = e.description().ok()?;

            if serial_number.is_empty() {
                None
            } else {
                Some(DeviceListEntry::D3xx {
                    serial_number,
                    description,
                })
            }
        })
        .collect())
}

/// Attempt to load the D3XX library.
///
/// First the library will attempt to be loaded from the executable directory/PATH, then from the bundled
/// library.
pub fn load_d3xx_library() -> Result<(), ConnectionError> {
    #[cfg(target_os = "windows")]
    const LIBRARY_NAME: &'static str = "FTD3XX.dll";

    #[cfg(target_os = "linux")]
    const LIBRARY_NAME: &'static str = "libftd3xx.so";

    match ft60x_rs::load_dylib(LIBRARY_NAME) {
        Ok(_) | Err(D3xxError::LibraryAlreadyLoaded) => Ok(()),
        Err(_) => ft60x_rs::load_bundled_dylib().or(Err(ConnectionError::Unknown)),
    }
}

// ====================================================================================================
/// Holds information about a UDP connection.
///
/// # Examples
/// ```ignore
/// let socket: Arc<UdpSocket> = ...;
/// let info = UdpConnectionInfo::new(&socket).expect("failed to read info");
/// println!("Info: {:?}", info);
/// ```
#[derive(Serialize, Deserialize, Debug, Clone, ToSchema)]
pub struct UdpConnectionInfo {
    /// The IP address of the board.
    pub board_ip: String,
    /// The port used for communication.
    pub board_port: u16,
    /// The IP address which the board sends data to.
    pub receiver_ip: String,
    /// The port which the board sends data to.
    pub receiver_port: u16,
}

impl UdpConnectionInfo {
    /// Construct a new [`UdpConnectionInfo`] from the given [`UdpSocket`].
    ///
    /// # Errors
    /// Returns a [`ConnectionError::Disconnected`] error if the socket is not connected.
    pub fn new(udp: &Arc<UdpSocket>) -> Result<UdpConnectionInfo, ConnectionError> {
        let local_addr = udp.local_addr().or(Err(ConnectionError::Disconnected))?;
        let peer_addr = udp.peer_addr().or(Err(ConnectionError::Disconnected))?;
        Ok(UdpConnectionInfo {
            board_ip: peer_addr.ip().to_string(),
            board_port: peer_addr.port(),
            receiver_ip: local_addr.ip().to_string(),
            receiver_port: local_addr.port(),
        })
    }
}
