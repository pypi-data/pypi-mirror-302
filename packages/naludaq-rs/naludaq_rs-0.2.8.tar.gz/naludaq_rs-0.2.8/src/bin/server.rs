//! Binary for running the backend server.

use std::{net::SocketAddr, path::PathBuf, str::FromStr};

use clap::Parser;

use naludaq_rs::web_api::serve_forever;

/// Default address to run the server at.
const DEFAULT_ADDR: &str = "127.0.0.1:7878";

/// Arguments for the server binary.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The address to host the server at. Expected format is "{HOST}:{PORT}"
    #[arg(short, long, default_value = DEFAULT_ADDR)]
    addr: String,
    /// The output directory for acquisitions
    #[arg(short, long, default_value = None)]
    output: Option<PathBuf>,
    /// Show debug messages
    #[arg(short, long, default_value_t = false)]
    debug: bool,
    /// Open the Swagger API in the browser
    #[arg(long, default_value_t = false)]
    api: bool,
    /// The directory to store log files in
    #[arg(long, default_value = None)]
    log_dir: Option<PathBuf>,
}

/// Runs the server using the specified arguments.
///
/// See [`crate::Args`] for the available arguments.
#[tokio::main]
async fn main() {
    // address args
    let args = Args::parse();
    let addr = match SocketAddr::from_str(args.addr.as_str()) {
        Ok(addr) => addr,
        Err(_) => {
            eprintln!("Invalid address, expected format is HOST_IP:PORT");
            std::process::exit(1);
        }
    };

    // output args
    let output_dir = args
        .output
        .unwrap_or(std::env::current_dir().expect("invalid working directory"));
    if !output_dir.is_dir() {
        eprintln!("Invalid output directory: {:?}", output_dir);
        std::process::exit(1);
    };

    // log args
    match setup_log_handler(args.log_dir, args.debug) {
        Ok(()) => {}
        Err(_) => {
            eprintln!("Invalid log directory");
            std::process::exit(1);
        }
    };

    if naludaq_rs::connection::load_d3xx_library().is_err() {
        tracing::warn!("The D3XX library could not be loaded: D3XX devices will not be usable.");
    }

    serve_forever(addr, output_dir, args.api).await;
    tracing::debug!("Exiting")
}

/// Set up and install the log handler.
fn setup_log_handler(log_dir: Option<PathBuf>, debug: bool) -> Result<(), logging::Error> {
    logging::LogHandlerBuilder::new()
        .debug(debug)
        .show_sources(true)
        .log_dir(log_dir)
        .create()
        .and_then(|handler| {
            handler.install()?;
            Ok(())
        })
}
