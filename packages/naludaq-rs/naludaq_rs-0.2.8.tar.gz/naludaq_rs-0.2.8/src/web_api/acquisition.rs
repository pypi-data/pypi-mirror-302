//! Module containing endpoints for accessing acquisitions.

use std::{collections::HashMap, fs, str::FromStr};

use axum::{
    body::Bytes,
    extract::{Query, State},
    Json,
};
use naluacq::{
    acquisition::{Metadata, MiscData, MiscDataKind},
    list_acquisitions, list_acquisitions_async, Acquisition, AcquisitionError,
};
// use hyper::StatusCode;

use super::{
    errors::{RequestError, Result},
    models::{
        AcquisitionDetails, AcquisitionList, AcquisitionMetadata, AcquisitionMoveRequest,
        AcquisitionName, AcquisitionShowAllParams, AcquisitionShowParams, AllAcquisitionDetails,
        EventLocator, MiscDataLocator, OutputAcquisition,
    },
    state::ServerState,
};
/// Create a new acquisition.
///
/// Creates a new acquisition in the root directory of the server.
/// The acquisition cannot already exist.
#[utoipa::path(
    post,
    path = "/acq",
    params(AcquisitionName),
    request_body=AcquisitionMetadata,
    responses(
        (status = 200, description = "Acquisition created successfully"),
        (status = 400, description = "Acquisition name is invalid"),
        (status = 500, description = "Server failed to create acquisition")
    ),
)]
#[tracing::instrument(err, skip_all)]
pub async fn create(
    State(state): State<ServerState>,
    Query(name): Query<AcquisitionName>,
    Json(metadata): Json<AcquisitionMetadata>,
) -> Result<Json<()>> {
    let acq_dir = state.root().join(&name.name);

    let metadata = Metadata::try_from(metadata.metadata).or(Err(RequestError::InvalidArguments))?;
    match Acquisition::create(acq_dir, &metadata) {
        Ok(_) => Ok(Json(())),
        Err(AcquisitionError::AlreadyExists) => Err(RequestError::AlreadyExists),
        Err(AcquisitionError::InvalidPath) => Err(RequestError::InvalidAcquisitionName),
        Err(_) => Err(RequestError::Unknown),
    }
}

/// Delete an acquisition.
///
/// Deletes an existing acquisition with the given name.
#[utoipa::path(
    delete,
    path = "/acq",
    params(AcquisitionName),
    responses(
        (status = 200, description = "Successfully deleted the acquisition",),
        (status=400, description="No acquisition with the given name"),
        (status=500, description="Server failed to delete acquisition"),
    ),
)]
#[tracing::instrument(err)]
pub async fn delete(
    State(state): State<ServerState>,
    Query(payload): Query<AcquisitionName>,
) -> Result<Json<()>> {
    let root = fs::canonicalize(state.root()).unwrap();
    let path = fs::canonicalize(state.root().join(&payload.name))
        .or(Err(RequestError::InvalidAcquisitionName))?;
    if !path.exists() || !path.is_dir() || !path.starts_with(root) {
        Err(RequestError::NoSuchAcquisition)?;
    }

    let worker = state.workers().storage_worker();
    if worker.output().await == Some(payload.name) {
        worker
            .set_output(None)
            .await
            .or(Err(RequestError::Unknown))?;
    }

    fs::remove_dir_all(path).or(Err(RequestError::Unknown))?;
    Ok(Json(()))
}

/// Get the output acquisition.
///
/// Gets the name of the acquisition currently used for data output.
#[utoipa::path(
    get,
    path = "/acq/output",
    responses(
        (status = 200, description = "Always", body=OutputAcquisition),
    ),
)]
#[tracing::instrument]
pub async fn get_output(State(state): State<ServerState>) -> Json<OutputAcquisition> {
    Json(OutputAcquisition {
        name: state.workers().storage_worker().output().await,
    })
}

/// Set the output acquisition.
///
/// Sets the name of the acquisition currently used for data output.
/// Must be an existing acquisition.
#[utoipa::path(
    put,
    path = "/acq/output",
    params(OutputAcquisition),
    responses(
        (status = 200, description = "Output changed successfully"),
        (status = 400, description = "No acquisition with the given name"),
    ),
)]
#[tracing::instrument(err)]
pub async fn set_output(
    State(state): State<ServerState>,
    Query(query): Query<OutputAcquisition>,
) -> Result<Json<()>> {
    state
        .workers()
        .storage_worker()
        .set_output(query.name)
        .await
        .or(Err(RequestError::NoSuchAcquisition))?;
    Ok(Json(()))
}

/// List all acquisitions.
///
/// Gets a list of all acquisitions existing in the root directory of the server.
#[utoipa::path(
    get,
    path = "/acq/list",
    responses(
        (
            status = 200,
            description = "Successfully retrieved acquisition information",
            body = AcquisitionList,
        ),
    ),
)]
#[tracing::instrument]
pub async fn list(State(state): State<ServerState>) -> Json<AcquisitionList> {
    let acqs: Vec<Acquisition> = list_acquisitions_async(state.root()).await;
    Json(AcquisitionList {
        acquisitions: acqs
            .iter()
            .map(|f| f.path().file_name().unwrap().to_str().unwrap().to_string())
            .collect(),
    })
}

/// Fetch acquisition details.
///
/// Gets a YAML-encoded string describing the acquisition.
#[utoipa::path(
    get,
    path = "/acq/show",
    params(AcquisitionShowParams),
    responses(
        (status = 200, description = "Successfully retrieved acquisition information", body = AcquisitionDetails),
        (status = 400, description = "No acquisition with the given name"),
    ),
)]
#[tracing::instrument(err)]
pub async fn show(
    State(state): State<ServerState>,
    Query(query): Query<AcquisitionShowParams>,
) -> Result<Json<AcquisitionDetails>> {
    let acq = Acquisition::open(state.root().join(&query.name))
        .or(Err(RequestError::NoSuchAcquisition))?;
    let fields = AcquisitionDetailsSelector::from(query);
    Ok(Json(details(acq, fields).await?))
}

/// Fetch details for all acquisitions.
#[utoipa::path(
    get,
    path = "/acq/show_all",
    params(AcquisitionShowAllParams),
    responses(
        (status = 200, description = "Successfully retrieved acquisition information", body = AllAcquisitionDetails),
        (status = 400, description = "No acquisition with the given name"),
    ),
)]
#[tracing::instrument(err)]
pub(crate) async fn show_all(
    State(state): State<ServerState>,
    Query(query): Query<AcquisitionShowAllParams>,
) -> Result<Json<AllAcquisitionDetails>> {
    let fields = AcquisitionDetailsSelector::from(query);
    let acqs = tokio::task::spawn_blocking(move || {
        list_acquisitions(state.root())
            .into_iter()
            .map(|f| Acquisition::open(f.path()))
            .collect::<Result<Vec<_>, _>>()
            .or(Err(RequestError::Unknown))
    })
    .await
    .or(Err(RequestError::Unknown))??;

    // fetching details needs to be done in parallel since reading many acquisitions
    // sequentially can take a long time
    let handles = acqs
        .iter()
        .map(|acq| tokio::spawn(details(acq.clone(), fields.clone())))
        .collect::<Vec<_>>();

    let mut details: HashMap<String, AcquisitionDetails> = HashMap::with_capacity(handles.len());
    for (handle, acq) in handles.into_iter().zip(acqs) {
        details.insert(acq.name(), handle.await.or(Err(RequestError::Unknown))??);
    }

    Ok(Json(AllAcquisitionDetails { details }))
}

/// Fetch an event from an acquisition.
///
/// Gets a single event from an acquisition as raw binary.
#[utoipa::path(
    get,
    path = "/acq/event",
    params(EventLocator),
    responses(
        (
            status = 200,
            description = "Successfully retrieved acquisition information",
            content_type="application/octet-stream"
        ),
        (status = 400, description = "No acquisition with the given name, or the index is out of bounds."),
    ),
)]
pub async fn event(
    State(state): State<ServerState>,
    Query(payload): Query<EventLocator>,
) -> Result<Vec<u8>> {
    let acq_path = state.root().join(payload.acquisition);

    tokio::task::spawn_blocking(move || {
        let acq = Acquisition::open(acq_path).or(Err(RequestError::NoSuchAcquisition))?;
        acq.get(payload.index)
            .or(Err(RequestError::EventIndexOutOfBounds))
    })
    .await
    .or(Err(RequestError::Unknown))?
}

/// Get misc data from an acquisition
#[utoipa::path(
    get,
    path = "/acq/misc_data",
    params(MiscDataLocator),
    responses(
        (
            status = 200,
            description = "Successfully retrieved misc data",
            content_type="application/octet-stream"
        ),
        (status = 400, description = "No acquisition with the given name or no such misc data"),
        (status = 500, description = "Server failed to read misc data"),
    ),
)]
pub async fn misc_data(
    State(state): State<ServerState>,
    Query(params): Query<MiscDataLocator>,
) -> Result<Vec<u8>> {
    let acq_path = state.root().join(params.acquisition);
    let misc_data_kind =
        MiscDataKind::from_str(&params.type_name).or(Err(RequestError::InvalidArguments))?;

    tokio::task::spawn_blocking(move || {
        let acq = Acquisition::open(acq_path).or(Err(RequestError::NoSuchAcquisition))?;
        match acq.misc_data(misc_data_kind) {
            Ok(data) => Ok(data.into_data()),
            Err(AcquisitionError::NoSuchMiscData) => Err(RequestError::InvalidArguments),
            Err(_) => Err(RequestError::Unknown),
        }
    })
    .await
    .or(Err(RequestError::Unknown))?
}

/// Set misc data for an acquisition
#[utoipa::path(
    put,
    path = "/acq/misc_data",
    params(MiscDataLocator),
    request_body(
        content = Vec<u8>,
        description = "Raw misc data",
        content_type = "application/octet-stream"
    ),
    responses(
        (status = 200, description = "Successfully set misc data"),
        (status = 400, description = "No acquisition with the given name or no such misc data"),
        (status = 500, description = "Server failed to write misc data"),
    ),
)]
pub async fn set_misc_data(
    State(state): State<ServerState>,
    Query(params): Query<MiscDataLocator>,
    body: Bytes,
) -> Result<Json<()>> {
    let acq_path = state.root().join(params.acquisition);
    let misc_data_kind =
        MiscDataKind::from_str(&params.type_name).or(Err(RequestError::InvalidArguments))?;
    let misc_data = MiscData::new(body.into(), misc_data_kind);

    tokio::task::spawn_blocking(move || {
        let acq = Acquisition::open(acq_path).or(Err(RequestError::NoSuchAcquisition))?;
        match acq.set_misc_data(&misc_data) {
            Ok(()) => Ok(Json(())),
            Err(_) => Err(RequestError::Unknown),
        }
    })
    .await
    .or(Err(RequestError::Unknown))?
}

/// Move acquisition from one place to another.
///
/// Currently this only works for renaming within the root directory
#[utoipa::path(
    put,
    path = "/acq/move",
    params(AcquisitionMoveRequest),
    responses(
        (status = 200, description = "Successfully moved acquisition"),
        (status = 400, description = "No acquisition with the given name or invalid destination name"),
        (status = 500, description = "Server failed to move the acquisition for an unknown reason"),
    ),
)]
pub async fn move_acquisition(
    State(state): State<ServerState>,
    Query(params): Query<AcquisitionMoveRequest>,
) -> Result<Json<()>> {
    let source = state.root().join(&params.source_name);
    let dest = state.root().join(&params.dest_name);

    tokio::task::spawn_blocking(move || {
        let mut acq = Acquisition::open(source).or(Err(RequestError::InvalidAcquisitionName))?;
        match acq.move_to(dest) {
            Ok(()) => Ok(Json(())),
            Err(AcquisitionError::InvalidPath | AcquisitionError::AlreadyExists) => {
                Err(RequestError::InvalidArguments)
            }
            Err(_) => Err(RequestError::Unknown),
        }
    })
    .await
    .or(Err(RequestError::Unknown))?
}

async fn details(
    acq: Acquisition,
    fields: AcquisitionDetailsSelector,
) -> Result<AcquisitionDetails> {
    macro_rules! filter {
        ($cond: expr, $ok: expr) => {
            match $cond {
                None | Some(0) => None,
                Some(_) => Some($ok),
            }
        };
    }
    tokio::task::spawn_blocking(move || {
        let mut details = AcquisitionDetails::default();
        details.path = filter!(fields.path, acq.path().to_str().unwrap().to_string());
        details.metadata = filter!(
            fields.metadata,
            acq.metadata_str().or(Err(RequestError::Unknown))?
        );
        details.len = filter!(fields.len, acq.len().or(Err(RequestError::Unknown))?);
        details.chunk_count = filter!(fields.chunk_count, acq.chunk_count());
        details.total_size = filter!(
            fields.total_size,
            acq.total_size().or(Err(RequestError::Unknown))?
        );
        Ok(details)
    })
    .await
    .or(Err(RequestError::Unknown))?
}

/// Common container for acq detail selection. A serde bug prevents
/// us from using a struct with optional fields directly as a query
/// in combination with `#[serde(flatten)]`.
#[derive(Clone, Debug)]
pub struct AcquisitionDetailsSelector {
    pub path: Option<usize>,
    pub metadata: Option<usize>,
    pub len: Option<usize>,
    pub chunk_count: Option<usize>,
    pub total_size: Option<usize>,
}

impl From<AcquisitionShowAllParams> for AcquisitionDetailsSelector {
    fn from(params: AcquisitionShowAllParams) -> Self {
        Self {
            path: params.path,
            metadata: params.metadata,
            len: params.len,
            chunk_count: params.chunk_count,
            total_size: params.total_size,
        }
    }
}

impl From<AcquisitionShowParams> for AcquisitionDetailsSelector {
    fn from(params: AcquisitionShowParams) -> Self {
        Self {
            path: params.path,
            metadata: params.metadata,
            len: params.len,
            chunk_count: params.chunk_count,
            total_size: params.total_size,
        }
    }
}
