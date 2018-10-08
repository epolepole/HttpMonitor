#!/usr/bin/env python
import logging

from common import configuration_reader
from common.configuration_reader import Options
from common.input_args_parser import get_args
from common.logger_configuration import configure_logging
from displayers.displayer_factory import DisplayerFactory
from http_monitor_builder import HttpMonitorBuilder
from monitors.avg_alert_bundle import AvgAlertBundle
from monitors.basic_stats_bundle import BasicStatsBundle

logger = logging.getLogger(__name__)


def print_callback(data):
    print(str(data))


def main():
    line_args = get_args()
    opts = Options()
    opts.log_file_path = line_args.file_to_monitor
    configuration_reader.get_config(line_args.config_file, opts)
    configure_logging(opts.debug, opts.log_to_file, opts.log_to_stdout)
    displayer = DisplayerFactory.manufacture_displayer(opts.disp_type, opts.output_file)

    http_monitor_builder = HttpMonitorBuilder(opts.log_file_path)

    for alert_param in opts.alert_parameters:
        logger.info("Alert when traffic over {} for at least {} seconds".format(alert_param[0], alert_param[1]))
        avg_alert_bundle = AvgAlertBundle(alert_param[0], alert_param[1], displayer.display)
        http_monitor_builder.add_monitor(avg_alert_bundle)

    if opts.stats_interval > 0:
        logger.info('Using stats monitor every {} seconds'.format(opts.stats_interval))
        basic_stats_bundle = BasicStatsBundle(opts.stats_interval, displayer.display)
        http_monitor_builder.add_monitor(basic_stats_bundle)

    http_monitor_builder.get_monitor().start()


if __name__ == "__main__":
    main()
