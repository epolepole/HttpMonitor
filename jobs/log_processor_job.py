import heapq

from bom.average_stats import AverageStats
from jobs.abstract_job import AbstractJob


class LogProcessorJob(AbstractJob):
    def __init__(self, input_queue: list, output_stats: AverageStats, interval=0.1):
        super().__init__(interval)
        self.__input_pq = input_queue
        self.__output_stats = output_stats

    def _iteration(self):
        while len(self.__input_pq) != 0:
            log = heapq.heappop(self.__input_pq)
            self.__output_stats.increment_trx_at(log.second)
