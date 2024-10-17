//! Module for generating OpenAPI documentation.
//!
//! The Swagger UI is hosted under the `/api` route.
//!
//! Uses [utoipa] to generate the documentation, and  [`utoipa_swagger_ui`] for
//! the Swagger UI endpoint.
//!
use std::{net::SocketAddr, time::Duration};

use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

use super::{acquisition, board, config, connection, models};
use crate::connection::{
    ConnectionInfo, D2xxConnectionInfo, SerialConnectionInfo, UdpConnectionInfo, DeviceListEntry
};

/// OpenAPI documentation for the server.
///
/// This is generated at compile-time.
/// Make sure to keep it updated!
#[derive(utoipa::OpenApi)]
#[openapi(
    paths(
        acquisition::create,
        acquisition::get_output,
        acquisition::set_output,
        acquisition::show,
        acquisition::show_all,
        acquisition::event,
        acquisition::list,
        acquisition::delete,
        acquisition::misc_data,
        acquisition::set_misc_data,
        acquisition::move_acquisition,
        board::write,
        board::read,
        config::set_packager_configuration,
        config::shutdown,
        connection::connect_udp,
        connection::configure_serial,
        connection::configure_d2xx,
        connection::connect_d3xx,
        connection::disconnect,
        connection::clear_buffers,
        connection::connection_info,
        connection::list_connections,
        config::debug_info,
    ),
    components(schemas(
        models::AcquisitionMetadata,
        models::OutputAcquisition,
        models::AcquisitionDetails,
        models::AllAcquisitionDetails,
        models::AcquisitionList,
        models::DataPackages,
        models::DeviceList,
        models::ConnectionInfoResponse,
        DeviceListEntry,
        ConnectionInfo,
        UdpConnectionInfo,
        SerialConnectionInfo,
        D2xxConnectionInfo,
        models::D2xxConfiguration,
        models::D3xxConfiguration,
        models::D2xxTimeouts,
        models::SystemInfo,
    ))
)]
pub struct ApiDoc;

/// Get a [`SwaggerUi`] instance for viewing/calling the API.
pub fn ui() -> SwaggerUi {
    let config = utoipa_swagger_ui::Config::new(["/openapi.json"])
        .use_base_layout()
        .try_it_out_enabled(true);

    SwaggerUi::new("/api")
        .config(config)
        .url("/openapi.json", ApiDoc::openapi())
}

/// Open the API docs with the system browser.
pub async fn open_docs(server_addr: SocketAddr) {
    tokio::time::sleep(Duration::from_millis(100)).await;
    open::that(format!("http://{}/api", server_addr)).unwrap();
}
