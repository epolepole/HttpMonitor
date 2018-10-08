import configparser

from displayers.displayer_factory import Displayers

ALERTS = "Alerts"
OUTPUT = "Output"
STATS = "Stats"
LOGGING = "Logging"


class Options:
    def __init__(self):
        self.log_file_path = ""
        self.stats_interval = 10
        self.alert_parameters = [(300, 120)]
        self.disp_type = Displayers.LOG
        self.output_file = ""
        self.debug = False
        self.log_to_stdout = False
        self.log_to_file = ""


def compute_alerts(config, args):
    if ALERTS in config.sections():
        args.alert_parameters.clear()
        for alert in config.options(ALERTS):
            threshold, time_frame = map(int, config.get(ALERTS, alert).split(','))
            if threshold > 0 and time_frame > 0:
                args.alert_parameters.append((threshold, time_frame))


def get_config(config_path: str, opts: Options):
    config = configparser.ConfigParser()
    config.read("default.cfg")
    config.read(config_path)

    opts.stats_interval = config.getint(STATS, "interval")

    compute_alerts(config, opts)

    opts.disp_type = Displayers(config.get(OUTPUT, "displayer"))
    if opts.disp_type == Displayers.FILE:
        opts.disp_type = Displayers(config.get(OUTPUT, "file_name"))

    opts.debug = config.getboolean(LOGGING, "debug")
    opts.log_to_stdout = config.getboolean(LOGGING, "log_to_stdout")
    try:
        opts.log_to_file = config.get(LOGGING, "log_to_file")
    except:
        pass
