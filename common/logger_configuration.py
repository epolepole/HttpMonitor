import logging
import sys


def configure_logging(is_debug=False, log_to_file=False, log_file='http_log_monitor.log', log_to_stdout=False):
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(name)s - %(message)s")
    handlers = []
    if log_to_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(log_formatter)
        handlers.append(file_handler)
    if log_to_stdout:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        handlers.append(console_handler)
    logging.basicConfig(level=logging.DEBUG if is_debug else logging.INFO, handlers=handlers)
