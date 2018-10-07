#!/usr/bin/env python
import logging
import time

from common.get_args import get_args
from common.logger_configuration import configure_logging
from displayers.displayer_factory import DisplayerFactory
from http_monitor_builder import HttpMonitorBuilder
from monitors.avg_alert_bundle import AvgAlertBundle
from monitors.basic_stats_bundle import BasicStatsBundle

logger = logging.getLogger(__name__)


def print_callback(data):
    print(str(data))


def main():
    args = get_args()
    configure_logging(args.debug, args.log_to_file, args.log_to_stdout)
    displayer = DisplayerFactory.manufacture_displayer(args.disp_type, args.output_file)

    http_monitor_builder = HttpMonitorBuilder(args.log_file_path)

    for alert_param in args.alert_parameters:
        logger.info("Alert when traffic over {} for at least {} seconds".format(alert_param[0], alert_param[1]))
        avg_alert_bundle = AvgAlertBundle(alert_param[0], alert_param[1], displayer.display)
        http_monitor_builder.add_monitor(avg_alert_bundle)

    if args.stats_interval != 0:
        logger.info('Using stats monitor every {} seconds'.format(args.stats_interval))
        basic_stats_bundle = BasicStatsBundle(args.stats_interval, displayer.display)
        http_monitor_builder.add_monitor(basic_stats_bundle)

    with http_monitor_builder.get_monitor():
        while True:
            time.sleep(5)


if __name__ == "__main__":
    main()
