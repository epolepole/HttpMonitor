import datetime
from queue import PriorityQueue, Queue

from jobs.log_formatter_job import LogFormatterJob


def create_basic_log_queue():
    str_queue = Queue()
    str_queue.put(r'127.0.0.1 - james [09/May/2018:16:00:55 +0000] "GET /personal/create HTTP/1.0" 200 1234')
    str_queue.put(r'127.0.0.1 - james [09/May/2018:16:00:50 +0000] "GET /report HTTP/1.0" 200 1234')
    str_queue.put(r'127.0.0.1 - james [09/May/2018:16:01:00 +0000] "GET /api HTTP/1.0" 200 1234')
    return str_queue


def test_log_formats_correspondent_queue():
    str_log_queue = create_basic_log_queue()
    bom_log_queue = PriorityQueue()
    a_formatter = LogFormatterJob(str_log_queue, bom_log_queue, 0.1)
    a_formatter.loop(blocking=False)
    a_formatter.loop(blocking=False)
    log_1 = bom_log_queue.get()
    log_2 = bom_log_queue.get()
    assert log_1.resource == "/report"
    assert log_1.timestamp == datetime.datetime(2018, 5, 9, 16, 0, 50, tzinfo=datetime.timezone.utc)
    assert log_2.resource == "/personal/create"
    assert log_2.client_ip == "127.0.0.1"

    a_formatter.loop(blocking=False)
    log_3 = bom_log_queue.get()
    assert log_3.resource == "/api"
    assert log_3.method == "GET"


def test_logs_are_added_prioritized_based_on_timestamp():
    str_log_queue = create_basic_log_queue()
    bom_log_queue = PriorityQueue()
    a_formatter = LogFormatterJob(str_log_queue, bom_log_queue, 0.1)
    a_formatter.loop(blocking=False)
    a_formatter.loop(blocking=False)
    a_formatter.loop(blocking=False)
    log_1 = bom_log_queue.get()
    log_2 = bom_log_queue.get()
    log_3 = bom_log_queue.get()
    assert log_1.timestamp == datetime.datetime(2018, 5, 9, 16, 0, 50, tzinfo=datetime.timezone.utc)
    assert log_2.timestamp == datetime.datetime(2018, 5, 9, 16, 0, 55, tzinfo=datetime.timezone.utc)
    assert log_3.timestamp == datetime.datetime(2018, 5, 9, 16, 1, 00, tzinfo=datetime.timezone.utc)
