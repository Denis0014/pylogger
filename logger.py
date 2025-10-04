import logging
from typing import Callable, Optional
from tqdm import tqdm
from logging import Handler, LogRecord, Formatter

GREY = "\x1b[38;20m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = "[%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)d/%(funcName)s] %(message)s"

LEVEL_FORMATS = {
    logging.DEBUG: GREY + LOG_FORMAT + RESET,
    logging.INFO: GREY + LOG_FORMAT + RESET,
    logging.WARNING: YELLOW + LOG_FORMAT + RESET,
    logging.ERROR: RED + LOG_FORMAT + RESET,
    logging.CRITICAL: BOLD_RED + LOG_FORMAT + RESET,
}

class LoggingHandler(Handler):
    def __init__(
        self, 
        on_critical: Optional[Callable[[LogRecord], None]] = None, 
        on_error: Optional[Callable[[LogRecord], None]] = None, 
        on_warning: Optional[Callable[[LogRecord], None]] = None, 
        on_info: Optional[Callable[[LogRecord], None]] = None,
        on_debug: Optional[Callable[[LogRecord], None]] = None
    ):
        super().__init__()
        self.callbacks = {
            logging.CRITICAL: on_critical,
            logging.ERROR: on_error,
            logging.WARNING: on_warning,
            logging.INFO: on_info,
            logging.DEBUG: on_debug,
        }

    def format(self, record: LogRecord):
        log_fmt = LEVEL_FORMATS.get(record.levelno, LOG_FORMAT)
        formatter = Formatter(log_fmt, datefmt=TIME_FORMAT)
        return formatter.format(record)
    
    def handle(self, record: LogRecord):
        rv = super().handle(record)
        if not rv:
            return rv
        
        callback = self.callbacks.get(record.levelno)
        if callback:
            callback(record)
        return rv

    def emit(self, record: LogRecord):
        try:
            msg = self.format(record)
            tqdm.write(msg, end='\n')
        except RecursionError:
            raise
        except Exception as e:
            self.handleError(record)

def setup_logger(
        name: str,
        level: int = logging.INFO,
        on_critical: Optional[Callable[[LogRecord], None]] = None,
        on_error: Optional[Callable[[LogRecord], None]] = None,
        on_warning: Optional[Callable[[LogRecord], None]] = None,
        on_info: Optional[Callable[[LogRecord], None]] = None,
        on_debug: Optional[Callable[[LogRecord], None]] = None,
    ) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = LoggingHandler(
            on_critical=on_critical,
            on_error=on_error,
            on_warning=on_warning,
            on_info=on_info,
            on_debug=on_debug,
        )
        logger.addHandler(handler)

    return logger

def on_error(record: logging.LogRecord):
    print("Возникла ошибка")
    # Реалзация

def on_critical(record: logging.LogRecord):
    print("Возникла критическая ошибка")
    # Реалзация

mylogger = setup_logger(__name__, logging.INFO, on_error=on_error, on_critical=on_critical)

try:
    a= 1 / 0
except Exception as e:
    mylogger.error(e)
