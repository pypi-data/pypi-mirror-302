//! Module containing all the server-related functionality.
//!
//! The web server is built using [axum] and is controlled using the REST API.
//! For visual documentation on this API, use the `api` binary.
//!
//! The functionality of the server is broken down into several
//! [endpoints](https://developer.wordpress.org/rest-api/extending-the-rest-api/routes-and-endpoints)
//! which can be accessed through HTTP requests.
//!
//! The OpenAPI documentation is generated using [`utoipa`]. Developers, please make sure to keep
//! the documentation up to date.

mod acquisition;
pub mod api;
mod board;
mod config;
mod connection;
pub mod errors;
mod models;
mod site;
mod state;

use std::{net::SocketAddr, path::PathBuf, time::Duration};

use axum::{
    extract::DefaultBodyLimit,
    routing::{delete, get, post, put},
    Router,
};

use crate::web_api::state::ServerState;

/// Run the HTTP server at the given address and root directory.
///
/// The root directory is the directory which acquisitions will be accessed from.
pub async fn serve_forever(addr: SocketAddr, mut root: PathBuf, open_browser: bool) {
    // Root directory needs to be absolute, otherwise acquisition paths may
    // be relative to the working directory
    root = std::fs::canonicalize(&root).unwrap_or(root);

    tracing::info!("Creating server");
    let state = ServerState::new(root);
    let router = Router::new()
        // server configuration
        .route(
            "/server/data-format",
            put(config::set_packager_configuration),
        )
        .route("/server/shutdown", put(config::shutdown))
        .route("/server/debug-info", get(config::debug_info))
        // connection configuration
        .route("/connection/udp", put(connection::connect_udp))
        .route("/connection/serial", put(connection::configure_serial))
        .route("/connection/d2xx", put(connection::configure_d2xx))
        .route("/connection/d3xx", put(connection::connect_d3xx))
        .route("/connection/list", get(connection::list_connections))
        .route("/connection/info", get(connection::connection_info))
        .route("/connection/clear", put(connection::clear_buffers))
        .route("/connection/disconnect", put(connection::disconnect))
        // board I/O
        .route("/board/raw", put(board::write))
        .route("/board/raw", get(board::read))
        // acquisition access
        .route("/acq", post(acquisition::create))
        .route("/acq", delete(acquisition::delete))
        .route("/acq/output", put(acquisition::set_output))
        .route("/acq/output", get(acquisition::get_output))
        .route("/acq/event", get(acquisition::event))
        .route("/acq/show", get(acquisition::show))
        .route("/acq/show-all", get(acquisition::show_all))
        .route("/acq/list", get(acquisition::list))
        .route("/acq/move", put(acquisition::move_acquisition))
        .route(
            "/acq/misc-data",
            get(acquisition::misc_data).put(acquisition::set_misc_data),
        )
        // API
        .merge(api::ui())
        // Website
        .route("/", get(site::debug))
        .route("/index.html", get(site::debug))
        // state
        .with_state(state.clone())
        .layer(DefaultBodyLimit::disable());
    let server = axum::Server::bind(&addr).serve(router.into_make_service());
    let server_addr = server.local_addr();
    let server_shutdown = server.with_graceful_shutdown(shutdown_handler(state.clone()));
    let open_browser_fut = async move {
        if open_browser {
            api::open_docs(server_addr).await;
        }
    };

    tracing::info!("Running server on {:?}", addr);
    let _ = futures::join!(server_shutdown, state.workers().run(), open_browser_fut);
}

/// Shutdown hook. Stops the workers on Control+C signal.
async fn shutdown_handler(state: ServerState) {
    tokio::signal::ctrl_c()
        .await
        .expect("failed to install interrupt handler");
    tracing::warn!("Interrupted. Cleaning up...");
    state.workers().stop().await;
    tracing::debug!("Cleanup successful");
}

/// Try to ping the server at the given address, returning `true` if it responds.
///
/// This doesn't do a normal ping, but instead sends a request. This is because a normal ping
/// may succeed even if the server is not ready to accept requests.
pub async fn ping_server(addr: SocketAddr, timeout: Duration) -> bool {
    tokio::time::timeout(timeout, async move {
        let client = reqwest::Client::new();
        let url = format!("http://{addr}/the/route/does/not/matter");
        let interval = Duration::from_millis(10);
        loop {
            match client.get(&url).send().await {
                Ok(_) => break,
                Err(e) if e.is_status() => break,
                Err(_) => tokio::time::sleep(interval).await,
            }
        }
    })
    .await
    .is_ok()
}
