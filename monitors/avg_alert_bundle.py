from calculators.avg_stats_calculator import AvgStatsCalculator
from jobs.max_avg_transaction_alert import MaxAvgTransactionsAlert
from monitors.abstract_monitor_bundle import AbstractMonitorBundle


class AvgAlertBundle(AbstractMonitorBundle):
    def __init__(self, threshold, time_period, callback, interval=0.1):
        super().__init__()
        self.__average_stats_pqueue = list()
        self.calculator = AvgStatsCalculator(self.__average_stats_pqueue, time_period)
        self.job = MaxAvgTransactionsAlert(threshold, self.__average_stats_pqueue, callback, interval)
