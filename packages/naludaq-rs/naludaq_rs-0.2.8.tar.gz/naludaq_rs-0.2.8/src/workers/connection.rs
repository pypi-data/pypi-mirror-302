//! Worker for opening connections, reading, and writing.
//!
//! See the [worker documentation](crate::workers) for information regarding
//! the structure of a worker.
//!
//! # Interface Layer
//! The interface layer for the control worker has several functions
//! allowing the user to open connections and read from/write to the board.
//!
//! The connection is owned by the control layer, and may be retrieved at any time
//! through the [`ConnectionWorker::connection`] function
//!
//! # Control Layer
//! Available commands include opening connections, closing connections,
//! sending data, and retrieving the connection.
//!
//! The implementation layer is started only when a connection is opened,
//! and is stopped when the connection is dropped or the connection is changed.
//!
//! # Implementation Layer
//! The implementation layer simply reads data from the connection in a loop
//! and sends any received data through a channel to the [package worker](crate::workers::packager).
use std::{io::ErrorKind, net::SocketAddr, sync::Arc};

use flume::{Receiver, Sender};
use tokio::{net::UdpSocket, task::JoinHandle};

use crate::{
    connection::{Connection, D2xxConnection, SerialConnection, D3xxConnection},
    constants::{
        D2XX_READ_BUFFER_SIZE,
        SERIAL_READ_BUFFER_SIZE,
        UDP_HEADER_BYTES,
        UDP_READ_BUFFER_SIZE,
        D3XX_READ_BUFFER_SIZE,
        D3XX_CONNECT_TIMEOUT, D3XX_DUMMY_WORD,
    },
    error::{ConnectionError, ConnectionWorkerError},
    macros::{try_abort, unwrap_or_break},
    types::RawCommand,
};

use super::util::{WorkerCommand, WorkerResponse, WorkerResponseHandler};

/// A command for the connection worker.
///
/// This is sent from the interface layer to the control layer.
#[derive(Debug, Clone)]
enum CommandInner {
    /// Try connecting to a board using UDP.
    ConnectUdp {
        board_ip: SocketAddr,
        receiver_ip: SocketAddr,
    },
    /// Try connecting to a board using serial.
    ConnectSerial {
        /// COM port (windows) or path (linux)
        port: String,
        baud_rate: u32,
    },
    /// Try connecting to a board using D2xx.
    ConnectD2xx {
        serial_number: String,
        baud_rate: u32,
    },
    /// Try connecting to a board using D3xx.
    ConnectD3xx {
        serial_number: String,
    },
    /// Retrieve the current connection.
    GetConnection,
    /// Disconnect the current connection.
    Disconnect,
    /// Send data over an active connection.
    Send { data: Vec<u8> },
    /// Stop the worker.
    Stop,
}

/// A response to a [`Command`].
///
/// This is sent from the control layer to the interface layer.
#[derive(Debug, Clone)]
enum ResponseInner {
    /// No response necessary for the corresponding command
    None,
    /// Response for a [`Command::GetConnection`] command.
    Connection(Option<Connection>),
}

/// Alias for the response the control layer will send
/// in response to a [`Command`].
type ResponseResult = Result<ResponseInner, ConnectionWorkerError>;

/// Interface layer for the connection worker.
///
/// A connection must be initialized before any data can be read from/written to
/// the board.
#[derive(Clone, Debug)]
pub struct ConnectionWorker {
    /// Control-side channel for commands send to the worker.
    command_rx: Receiver<WorkerCommand<CommandInner>>,
    /// Control-side channel for command responses.
    response_tx: Sender<WorkerResponse<ResponseResult>>,
    /// Output channel for data received from a connection.
    from_board_tx: Sender<Vec<u8>>,
    /// Handler for responses from the implementation layer.
    response_handler: WorkerResponseHandler<CommandInner, ResponseResult>,
}

impl ConnectionWorker {
    /// Create a new connection worker.
    ///
    /// All data read from a connection is sent through the `from_board_tx` channel.
    ///
    /// The worker should be run with the [`ConnectionWorker::start`] method before
    /// performing any operations.
    pub fn new(from_board_tx: Sender<Vec<u8>>) -> Self {
        let (command_tx, command_rx) = flume::unbounded();
        let (response_tx, response_rx) = flume::unbounded();

        ConnectionWorker {
            command_rx: command_rx,
            response_tx: response_tx,
            from_board_tx: from_board_tx,
            response_handler: WorkerResponseHandler::new(command_tx, response_rx),
        }
    }

    /// Runs the worker. This method will run indefinitely until the worker is stopped.
    pub async fn start(&self) {
        let command_rx = self.command_rx.clone();
        let response_tx = self.response_tx.clone();
        let from_board_tx = self.from_board_tx.clone();
        run_connection_task_controller(command_rx, response_tx, from_board_tx).await;
    }

    /// Stops the worker. This method will not return until the control layer halts.
    pub async fn stop(&self) {
        let _ = self.request(CommandInner::Stop).await;
    }

    /// Query the control layer for the current [`Connection`].
    pub async fn connection(&self) -> Option<Connection> {
        match self.request(CommandInner::GetConnection).await {
            Ok(ResponseInner::Connection(x)) => x,
            _ => None,
        }
    }

    /// Try connecting to a board using UDP.
    ///
    /// The current connection, if any, will be dropped.
    ///
    /// # Errors
    /// A [`ConnectionWorkerError`] is returned if the connection could not be opened.
    pub async fn connect_udp(
        &self,
        board_ip: SocketAddr,
        receiver_ip: SocketAddr,
    ) -> Result<(), ConnectionWorkerError> {
        self.request(CommandInner::ConnectUdp {
            board_ip,
            receiver_ip,
        })
        .await
        .and(Ok(()))
    }

    /// Try connecting to a board using serial UART.
    ///
    /// The current connection, if any, will be dropped.
    ///
    /// # Errors
    /// A [`ConnectionWorkerError`] is returned if the connection could not be opened.
    pub async fn connect_serial(
        &self,
        port: &str,
        baud_rate: u32,
    ) -> Result<(), ConnectionWorkerError> {
        self.request(CommandInner::ConnectSerial {
            port: port.to_string(),
            baud_rate,
        })
        .await
        .and(Ok(()))
    }

    /// Try connecting to a board using D2XX.
    ///
    /// The current connection, if any, will be dropped.
    ///
    /// # Errors
    /// A [`ConnectionWorkerError`] is returned if the connection could not be opened.
    pub async fn connect_d2xx(
        &self,
        serial_number: &str,
        baud_rate: u32,
    ) -> Result<(), ConnectionWorkerError> {
        self.request(CommandInner::ConnectD2xx {
            serial_number: serial_number.to_string(),
            baud_rate,
        })
        .await
        .and(Ok(()))
    }

    /// Try connecting to a board using D3XX.
    ///
    /// The current connection, if any, will be dropped.
    ///
    /// # Errors
    /// A [`ConnectionWorkerError`] is returned if the connection could not be opened.
    pub async fn connect_d3xx(
        &self,
        serial_number: &str,
    ) -> Result<(), ConnectionWorkerError> {
        self.request(CommandInner::ConnectD3xx {
            serial_number: serial_number.to_string(),
        })
        .await
        .and(Ok(()))
    }

    /// Disconnect from the board.
    /// Has no effect if there is no connection.
    pub async fn disconnect(&self) -> Result<(), ConnectionWorkerError> {
        self.request(CommandInner::Disconnect).await.and(Ok(()))
    }

    /// Send a command to the board.
    ///
    /// # Errors
    /// A [`ConnectionWorkerError`] error is returned if the data could not be written
    /// or there is no connection
    pub async fn send_command(&self, data: RawCommand) -> Result<(), ConnectionWorkerError> {
        self.request(CommandInner::Send { data }).await.and(Ok(()))
    }

    /// Sends a [`Command`] to the control layer, and
    /// returns a [`Response`] indicating the operation status.
    async fn request(&self, command: CommandInner) -> ResponseResult {
        self.response_handler
            .request(command)
            .await
            .expect("connection worker request failed; the channels were dropped")
    }
}

/// Control layer for the connection worker.
///
/// Yields until the next command is received in the `command_rx` channel, then processes
/// the command and returns a response in the `response_tx` channel.
///
/// All data received from the socket is sent through the `from_board_tx` channel.
#[tracing::instrument(skip_all)]
async fn run_connection_task_controller(
    command_rx: Receiver<WorkerCommand<CommandInner>>,
    response_tx: Sender<WorkerResponse<ResponseResult>>,
    from_board_tx: Sender<Vec<u8>>,
) {
    let mut handle: Option<JoinHandle<()>> = None;
    let mut connection: Option<Connection> = None;
    let mut keep_alive: Option<Sender<()>> = None;

    loop {
        let WorkerCommand(id, command) = unwrap_or_break!(command_rx.recv_async().await);
        let response = match command {
            CommandInner::GetConnection => Ok(ResponseInner::Connection(connection.clone())),
            CommandInner::ConnectUdp {
                board_ip,
                receiver_ip,
            } => match UdpSocket::bind(receiver_ip).await {
                Ok(socket) => {
                    tracing::debug!("Dropping existing connection in order to connect UDP");
                    drop(keep_alive.take());
                    try_abort!(handle);
                    drop(connection.take());

                    match socket.connect(board_ip).await {
                        Ok(()) => {
                            let new_connection = Connection::Udp(Arc::new(socket));
                            tracing::debug!(
                                "Connected to board: {} via UDP",
                                &board_ip.to_string()
                            );
                            let (keep_alive_tx, keep_alive_rx) = flume::bounded(1);
                            handle = Some(tokio::spawn(run_reader_impl(
                                new_connection.clone(),
                                from_board_tx.clone(),
                                keep_alive_rx,
                            )));
                            keep_alive = Some(keep_alive_tx);
                            connection = Some(new_connection);
                            Ok(ResponseInner::None)
                        }
                        Err(e) => {
                            tracing::error!("Failed to connect UDP due to: {e:?}");
                            Err(ConnectionWorkerError::ConnectionFailed)
                        }
                    }
                }
                Err(_) => Err(ConnectionWorkerError::ConnectionFailed),
            },
            CommandInner::ConnectSerial { port, baud_rate } => {
                match SerialConnection::new(port, baud_rate).await {
                    Ok(serial) => {
                        tracing::debug!("Dropping existing connection in order to connect serial");
                        drop(keep_alive.take());
                        try_abort!(handle);
                        drop(connection.take());

                        let new_connection = Connection::Serial(serial);
                        let (keep_alive_tx, keep_alive_rx) = flume::bounded(1);
                        handle = Some(tokio::spawn(run_reader_impl(
                            new_connection.clone(),
                            from_board_tx.clone(),
                            keep_alive_rx,
                        )));
                        keep_alive = Some(keep_alive_tx);
                        connection = Some(new_connection);
                        Ok(ResponseInner::None)
                    }
                    Err(_) => Err(ConnectionWorkerError::ConnectionFailed),
                }
            }
            CommandInner::ConnectD2xx {
                serial_number,
                baud_rate,
            } => match D2xxConnection::new(&serial_number, baud_rate).await {
                Ok(device) => {
                    tracing::debug!("Dropping existing connection in order to connect D2XX");
                    drop(keep_alive.take());
                    try_abort!(handle);
                    drop(connection.take());

                    let new_connection = Connection::D2xx(device);
                    let (keep_alive_tx, keep_alive_rx) = flume::bounded(1);
                    handle = Some(tokio::spawn(run_reader_impl(
                        new_connection.clone(),
                        from_board_tx.clone(),
                        keep_alive_rx,
                    )));
                    keep_alive = Some(keep_alive_tx);
                    connection = Some(new_connection);
                    Ok(ResponseInner::None)
                }
                Err(_) => Err(ConnectionWorkerError::ConnectionFailed),
            },
            CommandInner::ConnectD3xx { serial_number } => {
                if connection.is_some() {
                    tracing::debug!("Dropping existing connection in order to connect D3XX");
                    drop(keep_alive.take());
                    try_abort!(handle);
                    drop(connection.take());
                }

                match D3xxConnection::new_with_timeout(&serial_number, &D3XX_CONNECT_TIMEOUT).await {
                    Ok(device) => {
                        let new_connection = Connection::D3xx(device);
                        let (keep_alive_tx, keep_alive_rx) = flume::bounded(1);
                        handle = Some(tokio::spawn(run_reader_impl(
                            new_connection.clone(),
                            from_board_tx.clone(),
                            keep_alive_rx,
                        )));
                        keep_alive = Some(keep_alive_tx);
                        connection = Some(new_connection);
                        Ok(ResponseInner::None)
                    }
                    Err(_) => Err(ConnectionWorkerError::ConnectionFailed),
                }
            },
            CommandInner::Disconnect => {
                drop(keep_alive.take());
                try_abort!(handle);
                drop(connection.take());
                Ok(ResponseInner::None)
            }
            CommandInner::Send { data } => {
                tracing::debug!("Sending command: {:02X?}", data);
                match connection {
                    Some(Connection::Udp(ref socket)) => match socket.send(data.as_slice()).await {
                        Ok(_) => Ok(ResponseInner::None),
                        Err(_) => Err(ConnectionWorkerError::SendFailed),
                    },
                    Some(Connection::Serial(ref serial)) => {
                        match serial.send(data.as_slice()).await {
                            Ok(_) => Ok(ResponseInner::None),
                            Err(_) => Err(ConnectionWorkerError::SendFailed),
                        }
                    }
                    Some(Connection::D2xx(ref d2xx)) => match d2xx.send(data.as_slice()).await {
                        Ok(_) => Ok(ResponseInner::None),
                        Err(_) => Err(ConnectionWorkerError::SendFailed),
                    },
                    Some(Connection::D3xx(ref d3xx)) => match d3xx.send(data.as_slice()).await {
                        Ok(_) => Ok(ResponseInner::None),
                        Err(_) => Err(ConnectionWorkerError::SendFailed),
                    },
                    None => Err(ConnectionWorkerError::NoConnection),
                }
            }
            CommandInner::Stop => {
                try_abort!(handle);
                let _ = response_tx.send(WorkerResponse(id, Ok(ResponseInner::None)));
                break;
            }
        };

        unwrap_or_break!(response_tx.send(WorkerResponse(id, response)));
    }
}

/// Implementation layer for the connection worker.
///
/// Reads a connection continually and sends data to the output channel.
/// If an error occurs while reading, the function immediately returns.
///
/// The maximum size of data received is determined by the connection type.
/// The values are [`UDP_READ_BUFFER_SIZE`], [`SERIAL_READ_BUFFER_SIZE`], and
/// [`D2XX_READ_BUFFER_SIZE`].
///
/// The `keep_alive` channel is used to interrupt the reader and exit.
/// This is currently necessary due to implementation details (a new runtime is created
/// which prevents the fn from being aborted).
///
/// For UDP, header bytes are stripped from each packet, up to [`UDP_HEADER_BYTES`] bytes.
#[tracing::instrument]
async fn run_reader_impl(
    connection: Connection,
    from_board_tx: flume::Sender<Vec<u8>>,
    keep_alive: flume::Receiver<()>,
) {
    let buf_size = match connection {
        Connection::Udp(_) => UDP_READ_BUFFER_SIZE,
        Connection::Serial(_) => SERIAL_READ_BUFFER_SIZE,
        Connection::D2xx(_) => D2XX_READ_BUFFER_SIZE,
        Connection::D3xx(_) => D3XX_READ_BUFFER_SIZE,
    };
    let mut buf: Vec<u8> = vec![0; buf_size];

    tracing::debug!("Running connection reader");

    // Different connection types need special handling.
    // Running synchronous readers in a new runtime gives a HUGE performance boost since otherwise
    // the reader will block the calling runtime.
    match connection {
        Connection::Udp(ref socket) => loop {
            match socket.recv(&mut buf).await {
                Ok(0) => {
                    tracing::error!("Error receiving data from the socket; aborting...");
                    break;
                }
                Ok(n) => {
                    if n <= UDP_HEADER_BYTES {
                        tracing::error!(
                            "Return package is malformed, check IP address and/or firmware."
                        );
                        break;
                    };
                    if from_board_tx
                        .send(buf[UDP_HEADER_BYTES..n].to_vec())
                        .is_err()
                    {
                        tracing::debug!("Output channel dropped; aborting...");
                        break;
                    }
                }
                Err(e) if e.kind() == ErrorKind::WouldBlock => (),
                Err(e) => {
                    tracing::error!("Error receiving data from the socket; aborting. Error: {e:?}");
                    break;
                }
            }

            if keep_alive.is_disconnected() {
                tracing::debug!("Received disconnect request; aborting...");
                break;
            }
        },
        Connection::Serial(serial) => tokio::task::spawn_blocking(move || {
            let runtime = tokio::runtime::Runtime::new().unwrap();
            runtime.block_on(async move {
                loop {
                    match serial.recv(&mut buf).await {
                        Ok(0) => (),
                        Ok(n) => {
                            if from_board_tx.send(buf[..n].to_vec()).is_err() {
                                tracing::debug!("Output channel dropped; aborting...");
                                break;
                            }
                        }
                        Err(ConnectionError::Timeout) => (),
                        Err(_) => {
                            tracing::error!("Error receiving data from the socket; aborting...");
                            break;
                        }
                    }

                    if from_board_tx.is_disconnected() || keep_alive.is_disconnected() {
                        tracing::debug!("Output channel dropped; aborting...");
                        break;
                    }
                }
            });
        })
        .await
        .unwrap(),
        Connection::D2xx(d2xx) => tokio::task::spawn_blocking(move || {
            let runtime = tokio::runtime::Runtime::new().unwrap();
            runtime.block_on(async move {
                loop {
                    match d2xx.recv(&mut buf).await {
                        Ok(0) => (),
                        Ok(n) => {
                            if from_board_tx.send(buf[..n].to_vec()).is_err() {
                                tracing::debug!("Output channel dropped; aborting...");
                                break;
                            }
                        }
                        Err(ConnectionError::Timeout) => (),
                        Err(_) => {
                            tracing::error!("Error receiving data from the device; aborting...");
                            break;
                        }
                    }
                    if from_board_tx.is_disconnected() || keep_alive.is_disconnected() {
                        tracing::debug!("Received disconnect request; aborting...");
                        break;
                    }
                }
            });
        })
        .await
        .unwrap(),
        Connection::D3xx(d3xx) => tokio::task::spawn_blocking(move || {
            let runtime = tokio::runtime::Runtime::new().unwrap();
            runtime.block_on(async move {
                loop {
                    if from_board_tx.is_disconnected() || keep_alive.is_disconnected() {
                        tracing::debug!("Received disconnect request; aborting...");
                        break;
                    }
                    match d3xx.recv(&mut buf).await {
                        Ok(n) if n >= 2 => {
                            if buf[..n] == D3XX_DUMMY_WORD {
                                continue;
                            }
                            if from_board_tx.send(buf[..n].to_vec()).is_err() {
                                tracing::debug!("Output channel dropped; aborting...");
                                break;
                            }
                        }
                        Ok(_) => (),
                        Err(ConnectionError::Timeout) => (),
                        Err(_) => {
                            tracing::error!("Error receiving data from the device; aborting...");
                            break;
                        }
                    }
                }
            });
        })
        .await
        .unwrap(),
    }
}
