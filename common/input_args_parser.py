import argparse


def get_args():
    parser = argparse.ArgumentParser(description='This tool monitors a log file and outputs stats based on the logs')
    parser.add_argument("-f", dest="file_to_monitor", default="/var/log/access.log", metavar='',
                        help="File to monitor. Default to /var/log/access.log")
    parser.add_argument("-c", dest="config_file", default="config.cfg", metavar='',
                        help="Configuration file with stats, alarms, and display options. Defaulted to config.cfg")

    return parser.parse_args()
