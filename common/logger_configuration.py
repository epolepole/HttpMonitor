import logging
import sys


def configure_logging(is_debug=False, log_file="", log_to_stdout=False):
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(name)s:%(lineno)s - %(message)s")
    handlers = []
    if log_file != "":
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(log_formatter)
        handlers.append(file_handler)
    if log_to_stdout:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        handlers.append(console_handler)
    logging.basicConfig(level=logging.DEBUG if is_debug else logging.INFO, handlers=handlers)
