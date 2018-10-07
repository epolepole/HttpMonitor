from jobs.max_avg_transaction_alert import MaxAvgTransactionsAlert
from monitors.abstract_monitor_bundle import AbstractMonitorBundle
from processors.avg_stats_processor import AvgStatsProcessor


class AvgAlertBundle(AbstractMonitorBundle):
    def __init__(self, threshold, time_period, callback, interval=0.1):
        super().__init__()
        self.__average_stats_pqueue = list()
        self.processor = AvgStatsProcessor(self.__average_stats_pqueue, time_period)
        self.job = MaxAvgTransactionsAlert(threshold, self.__average_stats_pqueue, callback, interval)
