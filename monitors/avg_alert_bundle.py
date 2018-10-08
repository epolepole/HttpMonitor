from queue import PriorityQueue, Queue

from monitors.abstract_monitor_bundle import AbstractMonitorBundle
from monitors.processors.avg_stats_processor import AvgStatsProcessor
from workers.max_avg_transaction_worker import MaxAvgTransactionsAlertWorker


class AvgAlertBundle(AbstractMonitorBundle):
    def __init__(self, threshold, time_period, callback, interval=0.01):
        self.__average_stats_pqueue = PriorityQueue()
        self.__threshold = threshold
        self.__time_period = time_period
        self.__callback = callback
        self.__interval = interval

    def get_processor(self):
        return AvgStatsProcessor(self.__average_stats_pqueue, self.__time_period)

    def get_worker(self, exception_queue: Queue):
        return MaxAvgTransactionsAlertWorker(self.__threshold, self.__average_stats_pqueue, self.__callback, self.__interval,
                                             exception_queue)
