# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.2.8] - 2024-08-21

### Fixed

- AAv3 parser failing data readout when reading less than all channels.


## [0.2.7] - 2024-07-08

### Added

- HDSoCv2 - add board model to the packager


## [0.2.6] - 2024-04-08

### Fixed

- UPAC96 - USB3 python connection now correctly calls the driver and can identify the connection.


## [0.2.5] - 2023-11-06

### Added

- Stub file for Python bindings

## [0.2.4] - 2023-10-22

### Fixed

- Bug in linear backoff for opening D3XX connections

## [0.2.3] - 2023-09-11

### Fixed

- Digital register reads failed due to mishandling of the response ID.

## [0.2.2] - 2023-08-30

### Fixed

- Acquisition paths returned by the web API could be returned as relative to the working directory when using the `-o` flag.

## [0.2.1] - 2023-08-27

### Fixed

- Build failed on Linux doe to connection needs different constructor on Linux and Windows.

## [0.2.0] - 2023-08-22

### Added

- d3xx driver support for USB3 transfer.

### Fixed

- Utoipa/swagger UI versions were incompatible, causing builds to fail in some cases

## [0.1.11] - 2023-08-15

### Changed

- The `naluacq` crate is now used for acquisition I/O

### Fixed

- Using immediate mode would sometimes lock up the server due to a bounded channel filling up


## [0.1.10] - 2023-07-26

### Fixed

- `__version__` attribute missing from package
- Concurrent requests which retrieved information from a worker had the potential to mismatch the responses


## [0.1.9] - 2023-06-16

### Added

- New endpoint for getting information about all acquisitions
- New parameter to `/acq/show` for selecting the data to fetch

### Changed

- Sped up acquisition listing


## [0.1.8] - 2023-04-28

### Changed

- Added a ping when starting server with python to confirm the server is started, returning a PyError if not.


## [0.1.7] - 2023-04-21

### Added

- Debug webpage for viewing server/system information

### Fixed:

- Linux CI build

### Fixed

- Packager now allows stop words of different lengths


## [0.1.6] - 2023-04-05

### Added

- Support for HDSoC

### Changed

- How the server handles endword for detecting the end of a datastream.


## [0.1.5] - 2023-03-28

### Changed

- Logging-related code broken out into `logging` workspace

### Fixed

- Could not create multiple server instances due to limitations of tracing crate


## [0.1.4] - 2023-03-24

### Fixed

- Logger did not work when using Python bindings due to prematurely-dropped log handler


## [0.1.3] - 2023-03-23

### Added

- CHANGELOG.md
