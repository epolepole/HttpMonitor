import logging
import os
from queue import Queue

import pytest

from workers.file_reader_worker import FileReaderWorker

logger = logging.getLogger(__name__)


def test_file_reader_fills_queue():
    output_queue = Queue()
    log_file_path = "./tmp.log"

    open(log_file_path, 'a').write("Testing line\n")
    a_file_reader_worker = FileReaderWorker(log_file_path, output_queue, 0.1)
    a_file_reader_worker.setup()

    open(log_file_path, 'a').write("log line 1\n")
    a_file_reader_worker._iteration()
    assert output_queue.get() == "log line 1"

    open(log_file_path, 'a').write("log line 2\n")
    a_file_reader_worker._iteration()
    assert output_queue.get() == "log line 2"

    open(log_file_path, 'a').write("log line 3\n")
    open(log_file_path, 'a').write("log line 4\n")
    a_file_reader_worker._iteration()
    assert output_queue.get() == "log line 3"
    assert output_queue.get() == "log line 4"

    a_file_reader_worker.tear_down()

    logger.debug("Removing file")
    if os.path.exists(log_file_path):
        os.remove(log_file_path)


def test_error_when_creating_watcher_from_non_existing_file():
    nonexistent_file_path = "./this/file/doesnt.exist"
    with pytest.raises(IOError):
        a_log_watcher = FileReaderWorker(nonexistent_file_path, Queue(), 0.1)
        a_log_watcher.setup()
