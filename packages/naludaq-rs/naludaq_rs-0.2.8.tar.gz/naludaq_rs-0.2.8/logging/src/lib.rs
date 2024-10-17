/// Crate containing utilities for logging to the console and to disk.
///
/// Currently, only one log handler can be installed per process.
/// All subsequent attempts to install a log handler will fail!
///
/// # Example
/// ```
/// fn setup_logging() -> Result<(), logging::Error> {
///     LogHandlerBuilder::new()
///         .log_dir(Some("some/directory"))
///         .interval(LogFileInterval::Hourly)
///         .debug(true)
///         .show_sources(true)
///         .create()?
///         .install()?;
///     Ok(())
/// }
///
/// ```
use std::path::PathBuf;

use once_cell::sync::OnceCell;
use tracing_appender::non_blocking::WorkerGuard;
use tracing_subscriber::{
    fmt, prelude::__tracing_subscriber_SubscriberExt, util::SubscriberInitExt, EnvFilter,
};

/// Name of the environment variable that controls the maximum log level.
const LOG_LEVEL_ENV_NAME: &str = "_LOG_LEVEL";

static HANDLER: OnceCell<LogHandler> = OnceCell::new();

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("failed to set global default subscriber")]
    AlreadyInstalled,
    #[error("failed to create log directory")]
    InvalidDirectory(#[from] std::io::Error),
    #[error("could not determine default directory")]
    NoDefaultDirectory,
}

pub type Result<T> = std::result::Result<T, Error>;

/// The interval at which log files are created by the rolling file appender.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LogFileInterval {
    /// Log files are created every hour.
    Hourly,
    /// Log files are created every day.
    Daily,
}

/// Attempt to install a default global log handler.
///
/// # Specifications
/// * The default log directory is hidden under the user's home directory.
///   On Windows, this is `%USERPROFILE%\AppData\Local\Nalu Scientific\logs`.
///   On Linux, this is `$XDG_DATA_HOME/Nalu Scientific/logs` or `$HOME/.local/share/Nalu Scientific/logs`.
/// * Log files are created every hour.
/// * Log files will include debug and source code information.
///
/// # Errors
/// * [`Error::AlreadyInstalled`] if a global default subscriber has already been installed.
/// * [`Error::InvalidDirectory`] if the default log directory could not be created.
/// * [`Error::NoDefaultDirectory`] if the default log directory could not be determined.
pub fn setup_default_global_logging() -> Result<()> {
    let handler = LogHandler {
        log_dir: default_directory()?,
        interval: LogFileInterval::Hourly,
        debug: true,
        show_sources: true,
        tracing_guard: None,
    };
    handler.install()?;
    Ok(())
}

/// Handler for logging.
///
/// While any number of [`LogHandler`]s may be created, only one may be installed.
pub struct LogHandler {
    /// Path to the log file directory.
    log_dir: PathBuf,
    /// Interval at which log files are created.
    interval: LogFileInterval,
    /// Whether to log debug messages.
    debug: bool,
    /// Whether to show source code information in log messages.
    show_sources: bool,
    /// Guard for the tracing appender.
    ///
    /// Must be kept alive to keep logging to disk.
    tracing_guard: Option<WorkerGuard>,
}

impl LogHandler {
    /// Install as the global default tracing subscriber.
    ///
    /// # Errors
    /// * [`Error::AlreadyInstalled`] if a global default subscriber has already been installed.
    pub fn install(mut self) -> Result<&'static LogHandler> {
        // The crazy return types of the tracing crate's functions make it hard to split this function up.
        // So, we just have one big function that does everything.

        let filter = self.env_filter();
        let subscriber_builder = tracing_subscriber::fmt()
            // Filter output
            .with_env_filter(filter)
            // Print to stdout
            .with_writer(std::io::stdout)
            // Use a more compact, abbreviated log format
            .compact()
            // Display source code file paths
            .with_file(self.show_sources)
            // Display source code line numbers
            .with_line_number(self.show_sources)
            // Display the thread ID an event was recorded on
            .with_thread_ids(self.show_sources)
            // Don't display the event's target (module path)
            .with_target(false)
            // Disable colorized output. Escape characters mess with the log files and command prompt
            .with_ansi(false)
            // Build the subscriber
            .finish();

        // Guard for tracing appender is kept to keep logging to file
        let (non_blocking, tracing_guard) = create_tracing_appender(&self.log_dir, self.interval);
        let file_writer_layer = fmt::Layer::new().with_writer(non_blocking).with_ansi(false);
        self.tracing_guard = Some(tracing_guard);
        subscriber_builder
            .with(file_writer_layer)
            .try_init()
            .or(Err(Error::AlreadyInstalled))?;
        HANDLER.set(self).or(Err(Error::AlreadyInstalled))?;
        // SAFETY:
        // The `HANDLER` is set above, so unwrapping the value below is safe.
        Ok(HANDLER.get().unwrap())
    }

    /// Get the path to the log directory, if one was set.
    pub fn path(&self) -> &PathBuf {
        &self.log_dir
    }

    /// Create the environment filter, used to filter out debug mesasges
    fn env_filter(&self) -> EnvFilter {
        let level = if self.debug { "debug" } else { "info" };
        std::env::set_var(LOG_LEVEL_ENV_NAME, format!("{}={}", "naludaq_rs", level));
        EnvFilter::from_env(LOG_LEVEL_ENV_NAME)
    }
}

/// Create a new rolling, non-blocking file appender for tracing.
/// The appender will create a new file every hour.
///
/// Returns the appender and a guard that must be kept alive to keep the appender alive.
fn create_tracing_appender(
    dir: &PathBuf,
    interval: LogFileInterval,
) -> (tracing_appender::non_blocking::NonBlocking, WorkerGuard) {
    let prefix = format!("proc {}", std::process::id());
    let file_appender = match interval {
        LogFileInterval::Hourly => tracing_appender::rolling::hourly,
        LogFileInterval::Daily => tracing_appender::rolling::daily,
    }(&dir, prefix);
    let (non_blocking, tracing_guard) = tracing_appender::non_blocking(file_appender);
    (non_blocking, tracing_guard)
}

/// Builder for the [`LogHandler`].
pub struct LogHandlerBuilder {
    /// Log file directory
    log_dir: Option<PathBuf>,
    /// Log file interval
    interval: LogFileInterval,
    /// Display debug messages
    debug: bool,
    /// Display source information
    show_sources: bool,
}

impl LogHandlerBuilder {
    /// Create a new log handler builder
    pub fn new() -> Self {
        Self {
            log_dir: None,
            debug: false,
            show_sources: false,
            interval: LogFileInterval::Hourly,
        }
    }

    /// Specify how log files are written to disk.
    ///
    /// If unspecified or `None`, a platform-specific default directory will be used.
    ///
    /// For Windows, the default directory is `%LOCALAPPDATA%\Nalu Scientific\logs`.
    /// For Linux, the default directory is `$XDG_DATA_HOME/Nalu Scientific/logs`
    /// or `$HOME/.local/share/Nalu Scientific/logs`.
    pub fn log_dir<P: AsRef<std::path::Path>>(&mut self, log_dir: Option<P>) -> &mut Self {
        self.log_dir = log_dir.map(|p| p.as_ref().to_path_buf());
        self
    }

    /// The interval at which log files are created.
    ///
    /// Default is [`LogFileInterval::Hourly`].
    pub fn log_interval(&mut self, interval: LogFileInterval) -> &mut Self {
        self.interval = interval;
        self
    }

    /// Specify whether to log debug information.
    ///
    /// Default is `false`.
    pub fn debug(&mut self, enable: bool) -> &mut Self {
        self.debug = enable;
        self
    }

    /// Specify whether to show source information in the output.
    ///
    /// Default is `false`.
    pub fn show_sources(&mut self, show: bool) -> &mut Self {
        self.show_sources = show;
        self
    }

    /// Create the log handler, but does not install it.
    ///
    /// # Errors
    /// * [`Error::InvalidDirectory`] if the log directory could not be created.
    /// * [`Error::NoDefaultDirectory`] if the default log directory could not be determined.
    pub fn create(&self) -> Result<LogHandler> {
        let log_dir = self.log_dir.clone().unwrap_or(default_directory()?);
        match std::fs::create_dir_all(&log_dir) {
            Err(e) if e.kind() != std::io::ErrorKind::AlreadyExists => {
                return Err(Error::InvalidDirectory(e))
            }
            _ => (),
        };

        Ok(LogHandler {
            log_dir,
            interval: self.interval,
            debug: self.debug,
            show_sources: self.show_sources,
            tracing_guard: None,
        })
    }
}

/// Get the default log directory.
///
/// This is the directory that will be used if no log directory is specified.
///
/// On Windows, this is `%LOCALAPPDATA%\Nalu Scientific\logs`.
/// On Linux, this is `$XDG_DATA_HOME/Nalu Scientific/logs` or `$HOME/.local/share/Nalu Scientific/logs`.
///
/// Errors:
/// * [`Error::NoDefaultDirectory`] if the default log directory could not be determined.
fn default_directory() -> Result<PathBuf> {
    let mut dir = dirs::data_local_dir().ok_or(Error::NoDefaultDirectory)?;
    dir.push("Nalu Scientific");
    dir.push("logs");
    Ok(dir)
}
