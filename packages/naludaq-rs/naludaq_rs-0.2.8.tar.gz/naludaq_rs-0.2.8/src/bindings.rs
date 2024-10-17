use std::{
    net::{SocketAddr, TcpStream},
    path::PathBuf,
    str::FromStr,
    time::Duration,
};

use ft60x_rs::D3xxError;
use pyo3::{
    exceptions::{PyOSError, PyTimeoutError, PyValueError},
    prelude::*,
};
use tokio::{runtime::Runtime, task::JoinHandle};

use crate::web_api::{ping_server, serve_forever};
use crate::error::ConnectionError;

/// Generous timeout for the server to start.
///
/// On some platforms it is necessary to allow the server some
/// time to start before it will accept requests.
const SERVER_BRINGUP_TIMEOUT: Duration = Duration::from_millis(1000);

/// Add bindings for naludaq_rs
#[pymodule]
pub(crate) fn naludaq_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_class::<Server>()?;
    Ok(())
}

#[pyclass]
struct Server {
    /// Address of the server
    addr: SocketAddr,
    /// Output directory of the server
    output: PathBuf,
    /// The tokio runtime the server is running on
    runtime: Runtime,
    /// Join handle for the server task.
    ///
    /// Is `None` if the server is not running.
    handle: Option<JoinHandle<()>>,
}

#[pymethods]
impl Server {
    /// Create a new server instance.
    ///
    /// The server instance is not started until the `start` method is called.
    /// It will run in the background until the `stop` method is called.
    ///
    /// This class is intended to be used from Python. It is not recommended to use this class directly.
    ///
    /// # Arguments
    /// * `addr` - The address to bind to
    /// * `output` - The output directory
    /// * `debug` - Whether to enable debug logging
    ///
    /// # Returns
    /// A new server instance
    ///
    /// # Example
    /// ```python
    ///     server = Server(
    ///     addr='127.0.0.1',
    ///     output='C:\\Users\\user\\Desktop\\output',
    /// )"
    /// ```
    ///
    #[new]
    pub fn __new__(_py: Python, addr: (String, u16), output: String) -> PyResult<Self> {
        let addr = SocketAddr::from_str(&format!("{}:{}", addr.0, addr.1)).unwrap();
        let output = PathBuf::from_str(&output).unwrap();
        let runtime = tokio::runtime::Runtime::new().unwrap();
        if load_d3xx_library().is_err() {
            tracing::warn!("The D3XX library could not be loaded: D3XX devices will not be usable.");
        }
        Ok(Self {
            addr,
            output,
            runtime,
            handle: None,
        })
    }

    /// Start the server
    ///
    /// This function starts the server operations in the background.
    /// It by using the attributes passed to the constructor.
    ///
    /// Blocks until the server is found to be responsive, or until the timeout
    /// specified by [`SERVER_BRINGUP_TIMEOUT`] is reached. If the server is unresponsive,
    /// it is stopped and an error is returned.
    ///
    /// # Errors
    /// * [`PyOSError`] if the server fails to start
    /// * [`PyTimeoutError`] if the server is unresponsive
    pub fn start<'a>(&mut self, _py: Python) -> PyResult<()> {
        match logging::setup_default_global_logging() {
            Ok(()) | Err(logging::Error::AlreadyInstalled) => {}
            Err(e) => return Err(PyOSError::new_err(e.to_string())),
        }

        let address = self.addr.clone();
        let output_dir = self.output.clone();
        self.handle = Some(
            self.runtime
                .spawn(serve_forever(address.clone(), output_dir, false)),
        );

        // server can take a while to start on some platforms,
        // need to wait for it to be ready
        let ping = self
            .runtime
            .block_on(ping_server(address, SERVER_BRINGUP_TIMEOUT));
        match ping {
            true => Ok(()),
            false => {
                let _ = self.stop(_py);
                Err(PyTimeoutError::new_err("Server is unresponsive"))
            }
        }
    }

    /// Stop the server
    ///
    /// This function stops the server operations.
    /// The server can be restarted by calling the `start` method again.
    pub fn stop<'a>(&mut self, _py: Python) -> PyResult<()> {
        if let Some(handle) = self.handle.take() {
            let address = self.addr.to_string();
            let client = reqwest::Client::new();
            let _guard = self.runtime.enter();
            futures::executor::block_on(async move {
                let _ = client
                    .put(format!("http://{}/server/shutdown", address))
                    .send()
                    .await;
            });
            handle.abort();
        }
        Ok(())
    }

    /// Check if the server is running.
    ///
    /// If the server has been previously started, this function will attempt to connect to the server
    /// in order to determine whether it is alive.
    ///
    /// This function is infalliable.
    fn is_running(&self) -> PyResult<bool> {
        match self.handle {
            Some(_) => TcpStream::connect(self.addr).map(|_| true).or(Ok(false)),
            None => Ok(false),
        }
    }

    /// Get the address of the server.
    ///
    /// This function is infalliable.
    #[getter]
    fn get_address(&self) -> PyResult<(String, u16)> {
        Ok((self.addr.ip().to_string(), self.addr.port()))
    }

    /// Get the output directory of the server.
    ///
    /// Errors:
    /// * [`PyValueError`] if the path is not valid utf-8
    #[getter]
    fn get_output_directory(&self) -> PyResult<String> {
        path_to_string(&self.output)
    }
}

/// Convert the given path to a string
///
/// # Errors
/// * [`PyValueError`] if the path is not valid utf-8
fn path_to_string(path: &PathBuf) -> PyResult<String> {
    Ok(path
        .to_str()
        .ok_or(PyValueError::new_err("path is not valid utf-8"))?
        .to_string())
}

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
