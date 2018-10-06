from queue import Queue

from bom.log import Log
from bom.log_builder import LogBuilder
from test.jobs.abstract_job import AbstractJob


class LogFormatterJob(AbstractJob):
    def __init__(self, str_log_input_queue: Queue, bom_log_output_queue: Queue, interval=0.01):
        super().__init__(interval)
        self.__input_queue = str_log_input_queue
        self.__output_queue = bom_log_output_queue

    def _iteration(self):
        self.__output_queue.put(LogBuilder(self.__input_queue.get()).get_log())


def create_basic_log_queue():
    str_queue = Queue()
    str_queue.put(r'127.0.0.1 - james [09/May/2018:16:00:50 +0000] "GET /report HTTP/1.0" 200 1234')
    str_queue.put(r'127.0.0.1 - james [09/May/2018:16:00:55 +0000] "GET /personal/create HTTP/1.0" 200 1234')
    str_queue.put(r'127.0.0.1 - james [09/May/2018:16:01:00 +0000] "GET /api HTTP/1.0" 200 1234')
    return str_queue


def test_log_formats_correspondent_queue():
    str_log_queue = create_basic_log_queue()
    bom_log_queue = Queue()
    a_formatter = LogFormatterJob(str_log_queue, bom_log_queue)
    a_formatter.loop(blocking=False)
    a_formatter.loop(blocking=False)
    a_log, b_log, c_log = Log(), Log(), Log()
    a_log.section = "report"
    b_log.section = "personal"
    c_log.section = "api"
    assert bom_log_queue.get() == a_log
    assert bom_log_queue.get() == b_log

    a_formatter.loop(blocking=False)
    assert bom_log_queue.get() == c_log

