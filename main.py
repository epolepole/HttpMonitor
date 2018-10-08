#!/usr/bin/env python
import logging
import sys

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
    opts = retrieve_options()
    configure_logging(opts.debug, opts.log_to_file, opts.log_to_stdout)
    logger.info("Watching file {}".format(opts.log_file_path))
    http_monitor = create_monitor(opts)
    return_code = 0
    try:
        http_monitor.start_workers()
    except KeyboardInterrupt or SystemExit:
        logger.info("Kill signal received")
    except Exception as ex:
        logger.error(str(ex))
        return_code = 1
    finally:
        http_monitor.stop_workers()
        sys.exit(return_code)


def create_monitor(opts):
    displayer = DisplayerFactory.manufacture_displayer(opts.disp_type, opts.output_file)
    http_monitor_builder = HttpMonitorBuilder(opts.log_file_path)
    setup_alerts(displayer, http_monitor_builder, opts)
    setup_monitor(displayer, http_monitor_builder, opts)
    http_monitor = http_monitor_builder.get_monitor()
    return http_monitor


def retrieve_options():
    line_args = get_args()
    opts = Options()
    opts.log_file_path = line_args.file_to_monitor
    configuration_reader.get_config(line_args.config_file, opts)
    return opts


def setup_monitor(displayer, http_monitor_builder, opts):
    if opts.stats_interval > 0:
        logger.info('Using stats monitor every {} seconds'.format(opts.stats_interval))
        basic_stats_bundle = BasicStatsBundle(opts.stats_interval, displayer.display)
        http_monitor_builder.add_monitor(basic_stats_bundle)


def setup_alerts(displayer, http_monitor_builder, opts):
    for alert_param in opts.alert_parameters:
        logger.info("Alert when traffic over {} for at least {} seconds".format(alert_param[0], alert_param[1]))
        avg_alert_bundle = AvgAlertBundle(alert_param[0], alert_param[1], displayer.display)
        http_monitor_builder.add_monitor(avg_alert_bundle)


if __name__ == "__main__":
    main()
