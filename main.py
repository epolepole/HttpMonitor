import logging
import time

from common import logger_configuration
from http_monitor_builder import HttpMonitorBuilder
from monitors.avg_alert_bundle import AvgAlertBundle
from monitors.basic_stats_bundle import BasicStatsBundle

logger_configuration.configure_logging(log_to_stdout=True, is_debug=False)
logger = logging.getLogger(__name__)


def print_callback(data):
    print(str(data))


def main():
    http_monitor_builder = HttpMonitorBuilder("tmp_log.log")
    avg_alert_bundle = AvgAlertBundle(30, 2, print_callback)
    http_monitor_builder.add_monitor(avg_alert_bundle)
    basic_stats_bundle = BasicStatsBundle(1, print_callback)
    http_monitor_builder.add_monitor(basic_stats_bundle)

    with http_monitor_builder.get_monitor():
        while True:
            time.sleep(5)


if __name__ == "__main__":
    main()
