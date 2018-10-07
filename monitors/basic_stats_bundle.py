from queue import PriorityQueue

from jobs.basic_stats_job import BasicStatsJob
from monitors.abstract_monitor_bundle import AbstractMonitorBundle
from processors.basic_stats_processor import BasicStatsProcessor


class BasicStatsBundle(AbstractMonitorBundle):
    def __init__(self, time_period, callback, interval=0.01):
        super().__init__()
        self.__basic_stats_pqueue = PriorityQueue()
        self.processor = BasicStatsProcessor(self.__basic_stats_pqueue, time_period)
        self.job = BasicStatsJob(self.__basic_stats_pqueue, callback, interval)
