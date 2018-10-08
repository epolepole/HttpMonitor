from queue import PriorityQueue, Queue

from monitors.abstract_monitor_bundle import AbstractMonitorBundle
from monitors.processors.basic_stats_processor import BasicStatsProcessor
from workers.basic_stats_worker import BasicStatsWorker


class BasicStatsBundle(AbstractMonitorBundle):
    def __init__(self, time_period, callback, interval=0.01):
        self.__time_period = time_period
        self.__callback = callback
        self.__interval = interval
        self.__basic_stats_pqueue = PriorityQueue()

    def get_processor(self):
        return BasicStatsProcessor(self.__basic_stats_pqueue, self.__time_period)

    def get_worker(self, exception_queue: Queue):
        return BasicStatsWorker(self.__basic_stats_pqueue, self.__callback, self.__interval, exception_queue)
