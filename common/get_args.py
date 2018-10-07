import argparse

from displayers.displayer_factory import Displayers


def get_args():
    parser = argparse.ArgumentParser(description='This tool monitors a log file and outputs stats based on the logs',
                                     usage="main.py -s interval [-a threshold timeperiod] [-f input_file] [--display display_mode [-o output_file]]")
    parser.add_argument('-f', '--input-log-file', dest='log_file_path', default='/var/log/access.log', type=str,
                        help='Absolute path to the log file to monitor', metavar='')

    monitors_group = parser.add_argument_group('available alerts')
    monitors_group.add_argument('-s', '--stats-interval', dest='stats_interval', required=True, type=int,
                                help='Frequency at which stats are showed. Input 0 for no stats', metavar='')
    monitors_group.add_argument('-a', '--alert', action='append', nargs=2, type=int, dest="alert_parameters", default=[],
                                help="<threshold> <time_period> Enable an alert when transactions go over threshold during time period", metavar='')

    config_group = parser.add_argument_group('configuration')
    config_group.add_argument('--display', dest='disp_type', type=Displayers, choices=list(Displayers),
                              default=Displayers.LOG, help='display method for application')
    config_group.add_argument('-o', '--output-file', dest='output_file', default='output.txt',
                              help='File where the application output will be written in case of selecting file displayer',
                              metavar='')
    #
    logging_group = parser.add_argument_group('logging settings')
    logging_group.add_argument('-d', action='store_true', dest='debug', default=False,
                               help='Activate debugging logs')

    logging_group.add_argument('--log-to-stdout', action='store_true', dest='log_to_stdout', default=False, help='Log to stdout')
    logging_group.add_argument('--log-to-file', dest='log_to_file', default="",
                               help='File where the application logs will be written. Leave empty for no log to file', metavar='')
    return parser.parse_args()
