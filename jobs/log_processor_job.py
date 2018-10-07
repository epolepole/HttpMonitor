import logging
from queue import PriorityQueue

from jobs.abstract_job import AbstractJob

logger = logging.getLogger(__name__)


class LogProcessorJob(AbstractJob):
    def __init__(self, input_queue: PriorityQueue, stats_processors: list, interval):
        super().__init__(interval)
        self.__input_pq = input_queue
        self.__stats_processors = stats_processors

    def _iteration(self):
        while not self.__input_pq.empty():
            log = self.__input_pq.get()
            for calculator in self.__stats_processors:
                calculator.process_log(log)
