from queue import PriorityQueue, Queue

from monitors.abstract_monitor_bundle import AbstractMonitorBundle
from monitors.monitor_jobs.basic_stats_job import BasicStatsJob
from monitors.processors.basic_stats_processor import BasicStatsProcessor


class BasicStatsBundle(AbstractMonitorBundle):
    def __init__(self, time_period, callback, interval=0.01):
        self.__time_period = time_period
        self.__callback = callback
        self.__interval = interval
        self.__basic_stats_pqueue = PriorityQueue()

    def get_processor(self):
        return BasicStatsProcessor(self.__basic_stats_pqueue, self.__time_period)

    def get_job(self, ex_queue: Queue):
        return BasicStatsJob(self.__basic_stats_pqueue, self.__callback, self.__interval, ex_queue)
