import logging
import sys


def configure_logging(log_file='http_log_monitor.log', is_debug=False):
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(name)s - %(message)s")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    logging.basicConfig(level=logging.DEBUG if is_debug else logging.INFO, handlers=[file_handler, console_handler])
