//! This module contains constants used throughout the library.

use std::time::Duration;

use crate::types::CommandId;

// =====================================================================================================
// Connection Constants
// =====================================================================================================
/// Number of header bytes in a UDP packet. Currently these headers are discarded.
pub const UDP_HEADER_BYTES: usize = 16;
/// Maximum number of bytes to read at a time for a UDP connection. As UDP is a datagram (non-streaming)
/// protocol, this value must be greater than the size of the largest packet sent over the connection.
pub const UDP_READ_BUFFER_SIZE: usize = 1500;
/// Maximum number of bytes to read at a time for a serial connection.
pub const SERIAL_READ_BUFFER_SIZE: usize = 4096;
/// Maximum number of bytes to read at a time for a D2XX connection.
pub const D2XX_READ_BUFFER_SIZE: usize = 4096;
/// Maximum number of bytes to read at a time for a D3XX connection.
pub const D3XX_READ_BUFFER_SIZE: usize = 4096;

/// Default timeout for serial operations.
pub const SERIAL_TIMEOUT: Duration = Duration::from_millis(10);
/// Default timeout for d2xx read operations.
pub const D2XX_READ_TIMEOUT: Duration = Duration::from_millis(5);
/// Default timeout for d2xx read operations.
pub const D2XX_WRITE_TIMEOUT: Duration = Duration::from_millis(5);
/// Default timeout for d3xx read operations.
pub const D3XX_READ_TIMEOUT: Duration = Duration::from_millis(5);
/// Default timeout for d3xx write operations.
pub const D3XX_WRITE_TIMEOUT: Duration = Duration::from_millis(5);
/// Default timeout for d3xx connections. This is necessary due to a
/// driver limitation.
///
/// After disconnecting from a device, the same device isn't immediately
/// available to reconnect to. This duration is a reasonable upper bound
/// for the driver cooldown period.
pub const D3XX_CONNECT_TIMEOUT: Duration = Duration::from_millis(800);

/// Default delay between consecutive connection attempts for D3XX connections.
///
/// If this value is too low the driver may not be able to connect
/// to the device at all.
pub const D3XX_CONNECTION_ATTEMPT_DELAY: Duration = Duration::from_millis(30);
/// D3XX connections always return a word regardless of whether or not
/// there's data available because it needs to return something when pinged.
/// This constant specifies the word returned by the firmware.
///
/// IMPORTANT: if someone writes a firmware with some other stop word,
/// kick and scream until they switch it to this one.
pub const D3XX_DUMMY_WORD: [u8; 2] = [0xFA, 0xCE];

// =====================================================================================================
// Packaging Constants
// =====================================================================================================
/// Maximum size of an answer package (inclusive).
///
/// Any packages longer than this value will be treated as an event
/// if the stop word matches the event stop word.
pub const MAX_ANSWER_PACKAGE_SIZE: usize = 16;

// =====================================================================================================
// Storage Constants
// =====================================================================================================
/// Default maximum file size for acquisition chunks.
pub const DEFAULT_CHUNK_CAPACITY: usize = 500_000_000;
/// Multiple of the disk page size to use for buffering the data file.
/// A small value will result in small but frequent writes, while a larger
/// value will result in large but infrequent writes. Too small or too large
/// a value will have a negative impact on performance.
pub const CHUNK_BUFFERING_FACTOR: usize = 256;
/// If no event was received for this long, the storager will automatically flush
/// the latest chunk to disk.
pub const STORAGE_FLUSH_TIMEOUT: Duration = Duration::from_millis(20);
/// The interval at which the storager polls for input. The storager may run faster than this value
/// if there is data awaiting.
pub const STORAGE_POLLING_INTERVAL: Duration = Duration::from_millis(5);
/// Enable storage logging
pub const ENABLE_STORAGE_LOGGING: bool = true;
/// Enable storage speed logging.
pub const ENABLE_STORAGE_SPEED_LOGGING: bool = true;
/// Latest chunk file version number
pub const LATEST_CHUNK_VERSION: usize = 1;

// =====================================================================================================
// Answer Worker Constants
// =====================================================================================================
/// Default timeout for register reads through any connection type.
/// This value should be greater than the timeout set for the current connection.
pub const REGISTER_READ_TIMEOUT: Duration = Duration::from_millis(50);
/// The maximum number of answers which are allowed to be stored. Any answers
/// inserted after this limit will result in the oldest answer being discarded.
pub const ANSWER_CACHE_SIZE: usize = 128;
/// The dummy answer ID used for digital register reads.
///
/// This is necessary because the digital register command/answer protocol
/// does not have a field for IDs (yet); all digital register reads are treated
/// as having the same ID.
pub const DUMMY_REGISTER_ID: CommandId = 0x00;

// =====================================================================================================
// Misc
// =====================================================================================================
/// Timeout for internal requests to worker implementation layers.
///
/// The timeout is set to a relatively high value because long requests are possible and not unexpected.
/// Since the workers are generally stable and well-behaved, a long timeout does not pose any issues for
/// the rest of the library.
pub const WORKER_IMPL_REQUEST_TIMEOUT: Duration = Duration::from_millis(5000);
