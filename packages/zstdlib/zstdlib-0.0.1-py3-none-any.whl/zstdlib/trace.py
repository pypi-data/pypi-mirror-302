import logging


def _define_logger_trace(LC: type, method: str, TRACE: int):
    # Define the function in the logger class, match name and help method style
    def trace(self, msg, *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'TRACE'.

        To pass exception information, use the keyword argument exc_info with
        a true TRACE, e.g.

        logger.trace("Houston, we have a %s", "tiny problem", exc_info=True)
        """
        self.log(TRACE, msg, *args, **kwargs)

    setattr(LC, method, trace)


def _define_logging_trace(method: str, TRACE: int):
    # Define the function in the logging module, match name and help method style
    def trace(msg, *args, **kwargs):
        """
        Log a message with severity 'TRACE' on the root logger. If the logger
        has no handlers, call basicConfig() to add a console handler with a
        pre-defined format.
        """
        logging.log(TRACE, msg, *args, **kwargs)

    setattr(logging, method, trace)


def install() -> None:
    """
    Install TRACE, logging.trace, getLogger().trace, etc into the logging module
    """
    if logging.DEBUG < 2:
        raise ValueError("logging.DEBUG is too small")
    TRACE: int = logging.DEBUG // 2
    name = "TRACE"
    method = name.lower()

    # Error check
    if hasattr(logging, name):
        raise AttributeError(f"logging module already has {name} defined")
    if hasattr(logging, method):
        raise AttributeError(f"logging module already has {method} defined")
    if hasattr(LC := logging.getLoggerClass(), method):
        raise AttributeError(f"logging.getLoggerClass() class already has {method} defined")

    # Add trace into the logging moule
    logging.addLevelName(TRACE, name)
    setattr(logging, name, TRACE)
    _define_logger_trace(LC, method, TRACE)
    _define_logging_trace(method, TRACE)
