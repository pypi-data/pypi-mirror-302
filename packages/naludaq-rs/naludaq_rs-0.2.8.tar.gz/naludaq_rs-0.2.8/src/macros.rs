//! Module containing useful macros.

#![allow(unused_macros)]
#![allow(unused_imports)]

/// Unwrap a [`Result`] or break the loop.
macro_rules! unwrap_or_break {
    ($result: expr) => {
        match $result {
            Ok(x) => x,
            Err(_) => break,
        }
    };
}

/// Unwrap a [`Result`] or continue the loop.
macro_rules! unwrap_or_continue {
    ($result: expr) => {
        match $result {
            Ok(x) => x,
            Err(_) => continue,
        }
    };
}
/// Attempt to abort an [`Option<JoinHandle>`](tokio::task::JoinHandle).
///
/// Sets the [`Option`] to `None`.
macro_rules! try_abort {
    ($handle: ident) => {
        match $handle {
            Some(ref x) => x.abort(),
            None => (),
        }
        drop($handle.take())
    };
}

pub(crate) use try_abort;
pub(crate) use unwrap_or_break;
pub(crate) use unwrap_or_continue;
