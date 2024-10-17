# Logging Crate

The `logging` crate provides a handler for logging that allows for filtering output, printing to standard output, and logging to a file.

# Usage
To set up a logger, create a new `LogHandlerBuilder`, specifying the directory where logs will be written, the interval at which to create new log files (either hourly or daily), whether to print debug messages, and whether to display source code information. Once the `LogHandler` instance has been created, it can be installed as the global default tracing subscriber by calling the `install` method.

The `install` method will create a new environment filter to be used to filter out debug messages, create a new subscriber, and use the specified settings to configure the subscriber. It will then create a new rolling, non-blocking file appender for tracing and set it as the global subscriber.

# Warning

Only one logger may be installed per process; all subsequent loggers will fail to install.
