import logging
import os
import time

import pytest
from mock import Mock, call

from common import logger_configuration
from http_monitor_builder import HttpMonitorBuilder
from monitors.avg_alert_bundle import AvgAlertBundle

logger_configuration.configure_logging(log_to_stdout=True, is_debug=True)
logger = logging.getLogger(__name__)

DEFAULT_LOG = '127.0.0.1 - james [09/May/2018:16:01:0{} +0000] "GET /api HTTP/1.0" 200 1234\n'


def init_file(log_file_path):
    open(log_file_path, 'w').write("First Line\n")


def write_log_lines(log_file_path, frequencies: list):
    with open(log_file_path, 'a') as log_file:
        for delta_sec, freq in enumerate(frequencies):
            for _ in range(freq):
                log_file.write(DEFAULT_LOG.format(delta_sec))
                log_file.flush()


def test_two_different_alarms_are_triggered():
    log_file_path = "./tmp.log"
    init_file(log_file_path)
    http_monitor_builder = HttpMonitorBuilder(log_file_path)
    mocked_callback = Mock()
    avg_alert_bundle_a = AvgAlertBundle(3, 3, mocked_callback, 0.01)
    avg_alert_bundle_b = AvgAlertBundle(4, 2, mocked_callback, 0.01)
    http_monitor_builder.add_monitor(avg_alert_bundle_a)
    http_monitor_builder.add_monitor(avg_alert_bundle_b)

    frequencies = [2, 4, 3, 3, 5, 2, 1, 1]

    http_monitor = http_monitor_builder.get_monitor()
    http_monitor.start_processes(blocking=False)
    write_log_lines(log_file_path, frequencies)
    time.sleep(1)
    http_monitor.stop_processes()

    logger.debug("Removing files")
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    calls = [
        call("High traffic generated an alert - hits = 3, triggered at 2018-05-09T18:01:02"),
        call("High traffic generated an alert - hits = 4, triggered at 2018-05-09T18:01:04"),
        call("High traffic alert recovered at 2018-05-09T18:01:05"),
        call("High traffic alert recovered at 2018-05-09T18:01:06")
    ]
    mocked_callback.assert_has_calls(calls, any_order=True)


def test_alert_is_triggered_and_released():
    log_file_path = "./tmp.log"
    init_file(log_file_path)
    http_monitor_builder = HttpMonitorBuilder(log_file_path)
    mocked_callback = Mock()
    avg_alert_bundle = AvgAlertBundle(3, 2, mocked_callback)
    http_monitor_builder.add_monitor(avg_alert_bundle)

    frequencies = [2, 4, 4, 3, 2, 1]
    http_monitor = http_monitor_builder.get_monitor()
    http_monitor.start_processes(blocking=False)
    write_log_lines(log_file_path, frequencies)
    time.sleep(1)
    http_monitor.stop_processes()

    logger.debug("Removing files")
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    calls = [
        call("High traffic generated an alert - hits = 3, triggered at 2018-05-09T18:01:01"),
        call("High traffic alert recovered at 2018-05-09T18:01:04")
    ]
    mocked_callback.assert_has_calls(calls)


def test_missing_file_stops_all_threads():
    log_file_path = "./non_existent_file.log"
    http_monitor_builder = HttpMonitorBuilder(log_file_path)
    mocked_callback = Mock()
    avg_alert_bundle = AvgAlertBundle(3, 2, mocked_callback)
    http_monitor_builder.add_monitor(avg_alert_bundle)
    http_monitor = http_monitor_builder.get_monitor()
    with pytest.raises(IOError):
        http_monitor.start_processes()
