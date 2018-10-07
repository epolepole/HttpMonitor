import heapq
import logging

from jobs.abstract_job import AbstractJob

logger = logging.getLogger(__name__)


class LogProcessorJob(AbstractJob):
    def __init__(self, input_queue: list, stats_processors: list, interval):
        super().__init__(interval)
        self.__input_pq = input_queue
        self.__stats_processors = stats_processors

    def _iteration(self):
        while len(self.__input_pq) != 0:
            log = heapq.heappop(self.__input_pq)
            for calculator in self.__stats_processors:
                calculator.process_log(log)
