//! Utilities for getting system information.
use once_cell::sync::OnceCell;
use std::collections::HashMap;

use serde::{Deserialize, Serialize};
use sysinfo::{CpuExt, DiskExt, NetworkExt, NetworksExt, ProcessExt, System, SystemExt, CpuRefreshKind};

/// System name. Only computed once when the first call to `SystemInfo::current()` is made.
static SYS_NAME: OnceCell<Option<String>> = OnceCell::new();
/// OS version. Only computed once when the first call to `SystemInfo::current()` is made.
static OS_VERSION: OnceCell<Option<String>> = OnceCell::new();
/// Kernel version. Only computed once when the first call to `SystemInfo::current()` is made.
static KERNEL_VERSION: OnceCell<Option<String>> = OnceCell::new();
/// Machine host name. Only computed once when the first call to `SystemInfo::current()` is made.
static HOST_NAME: OnceCell<Option<String>> = OnceCell::new();

/// Information about a single core
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CpuInfo {
    name: String,
    brand: String,
    vendor_id: String,
    /// CPU usage in percent
    usage: f32,
    /// CPU clock frequency in Hz
    frequency: u64,
}

impl From<&sysinfo::Cpu> for CpuInfo {
    fn from(cpu: &sysinfo::Cpu) -> Self {
        Self {
            name: cpu.name().to_owned(),
            brand: cpu.brand().to_owned(),
            vendor_id: cpu.vendor_id().to_owned(),
            usage: cpu.cpu_usage(),
            frequency: cpu.frequency(),
        }
    }
}

/// Information about a single disk
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DiskInfo {
    name: String,
    /// Total disk space in bytes
    total_space: u64,
    /// Available disk space in bytes
    available_space: u64,
}

impl From<&sysinfo::Disk> for DiskInfo {
    fn from(disk: &sysinfo::Disk) -> Self {
        Self {
            name: disk.name().to_string_lossy().into_owned(),
            total_space: disk.total_space(),
            available_space: disk.available_space(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkInfo {
    /// The total amount of received data in bytes.
    pub total_received: u64,
    /// The total amount of sent data in bytes.
    pub total_transmitted: u64,
}

impl From<&sysinfo::NetworkData> for NetworkInfo {
    fn from(network: &sysinfo::NetworkData) -> Self {
        Self {
            total_received: network.total_received(),
            total_transmitted: network.total_transmitted(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessInfo {
    /// The name of the process.
    pub name: String,
    /// The amount of memory used in bytes.
    pub memory: u64,
    /// Fraction of CPU usage by this process
    pub cpu_usage: f32,
    /// Total number of bytes written to disk by this process
    pub disk_bytes_written: usize,
    /// Total number of bytes read from disk by this process
    pub disk_bytes_read: usize,
    /// How long the process has been alive in seconds
    pub run_time: usize,
}

impl ProcessInfo {
    fn new(sys: &System, process: &sysinfo::Process) -> Self {
        Self {
            name: process.name().to_owned(),
            memory: process.memory(),
            cpu_usage: process.cpu_usage() / sys.cpus().len() as f32,
            run_time: process.run_time() as usize,
            disk_bytes_read: process.disk_usage().total_read_bytes as usize,
            disk_bytes_written: process.disk_usage().total_written_bytes as usize,
        }
    }
}

/// A whole bunch of system information.
///
/// Some fields are `Option`s. If they are `None` this indicates
/// the value is unknown.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemInfo {
    /// The name of the operating system.
    pub name: Option<String>,
    /// The kernel version.
    pub kernel_version: Option<String>,
    /// The operating system version.
    pub os_version: Option<String>,
    /// The name of the
    /// [host](https://en.wikipedia.org/wiki/Computer_host) computer.
    pub host_name: Option<String>,
    /// Information about each disk
    pub disks: Vec<DiskInfo>,
    /// Information about each CPU
    pub cpus: Vec<CpuInfo>,
    /// The total amount of memory in bytes.
    pub total_memory: u64,
    /// The amount of memory used in bytes.
    pub used_memory: u64,
    /// The total amount of swap memory in bytes.
    pub total_swap: u64,
    /// The amount of swap memory used in bytes.
    pub used_swap: u64,
    /// Network I/O speeds for the current process, grouped by interface name.
    pub networks: HashMap<String, NetworkInfo>,
    /// Process information
    pub process: ProcessInfo,
    /// Number of seconds since the computer was last booted
    pub up_time: usize,
}

impl SystemInfo {
    /// Get the current system information.
    ///
    /// Unavailable information will be replaced with "Unknown".
    ///
    /// This function will block the current thread for a short period of time.
    pub fn current() -> Self {
        // SAFETY: this will panic on unsupported platforms,
        // but those platforms aren't targeted anyway
        let pid = sysinfo::get_current_pid().unwrap();
        let sys = system();
        Self {
            name: SYS_NAME.get_or_init(|| sys.name()).clone(),
            kernel_version: KERNEL_VERSION.get_or_init(|| sys.kernel_version()).clone(),
            os_version: OS_VERSION.get_or_init(|| sys.long_os_version()).clone(),
            host_name: HOST_NAME.get_or_init(|| sys.host_name()).clone(),

            total_memory: sys.total_memory(),
            used_memory: sys.used_memory(),
            total_swap: sys.total_swap(),
            used_swap: sys.used_swap(),
            up_time: sys.uptime() as usize,

            cpus: cpus(&sys),
            disks: disks(&sys),
            networks: networks(&sys),

            // SAFETY: unwrap() is safe since we're retrieving info for the current process,
            // which must exist.
            process: process(&sys, pid).unwrap(),
        }
    }
}

/// Same as `SystemInfo::current()`
pub fn current_system_info() -> SystemInfo {
    SystemInfo::current()
}

/// Fetch a [`sysinfo::System`].
///
/// Only refreshes the information we need for this module.
///
/// This function will block for a short duration (length depends on the system)
/// before refreshing the process info in order to obtain more accurate values for some
/// fields which are computed based on a time delta.
fn system() -> System {
    // SAFETY: get_current_pid() will only fail for unsupported platforms
    // which we don't target, at least currently
    let pid = sysinfo::get_current_pid().expect("failed to retrieve PID");

    let mut sys = System::new();
    sys.refresh_cpu_specifics(CpuRefreshKind::everything());
    sys.refresh_process(pid);
    std::thread::sleep(System::MINIMUM_CPU_UPDATE_INTERVAL);
    sys.refresh_cpu_specifics(CpuRefreshKind::everything());
    sys.refresh_process(pid);

    sys.refresh_disks_list();
    sys.refresh_disks();
    sys.refresh_networks_list();
    sys.refresh_networks();
    sys.refresh_memory();
    sys
}

/// Fetch [`NetworkInfo`] from the given system information.
fn networks(sys: &sysinfo::System) -> HashMap<String, NetworkInfo> {
    sys.networks()
        .iter()
        .map(|(name, data)| (name.clone(), NetworkInfo::from(data)))
        .collect()
}

/// Fetch [`CpuInfo`] for each CPU.
fn cpus(sys: &sysinfo::System) -> Vec<CpuInfo> {
    sys.cpus().iter().map(CpuInfo::from).collect()
}

/// Fetch [`DiskInfo`] for each disk.
fn disks(sys: &sysinfo::System) -> Vec<DiskInfo> {
    sys.disks()
        .iter()
        .map(DiskInfo::from)
        .collect()
}

/// Fetch [`ProcessInfo`] for the given process.
///
/// Returns `None` if the PID is invalid.
fn process(sys: &sysinfo::System, pid: sysinfo::Pid) -> Option<ProcessInfo> {
    Some(ProcessInfo::new(sys, sys.process(pid)?))
}
