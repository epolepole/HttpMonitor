import logging

import pytest
from mock import Mock

from common import logger_configuration
from http_monitor_builder import HttpMonitorBuilder
from monitors.avg_alert_bundle import AvgAlertBundle

logger_configuration.configure_logging(log_to_stdout=True, is_debug=True)
logger = logging.getLogger(__name__)


def test_missing_file_stops_all_threads():
    log_file_path = "./non_existent_file.log"
    http_monitor_builder = HttpMonitorBuilder(log_file_path)
    mocked_callback = Mock()
    avg_alert_bundle = AvgAlertBundle(3, 2, mocked_callback)
    http_monitor_builder.add_monitor(avg_alert_bundle)
    http_monitor = http_monitor_builder.get_monitor()
    with pytest.raises(IOError):
        http_monitor.start_workers()
