import heapq
import logging

from jobs.abstract_job import AbstractJob

logger = logging.getLogger(__name__)


class LogProcessorJob(AbstractJob):
    def __init__(self, input_queue: list, output_calculators: list, interval):
        super().__init__(interval)
        self.__input_pq = input_queue
        self.__output_calculators = output_calculators

    def _iteration(self):
        while len(self.__input_pq) != 0:
            log = heapq.heappop(self.__input_pq)
            for calculator in self.__output_calculators:
                calculator.process_log(log)
