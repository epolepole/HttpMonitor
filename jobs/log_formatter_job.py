import heapq
from queue import Queue

from bom.log_parser import LogParser
from jobs.abstract_job import AbstractJob


class LogFormatterJob(AbstractJob):
    def __init__(self, str_log_input_queue: Queue, bom_log_output_queue: list, interval=0.1):
        super().__init__(interval)
        self.__input_queue = str_log_input_queue
        self.__output_queue = bom_log_output_queue

    def _iteration(self):
        while not self.__input_queue.empty():
            heapq.heappush(self.__output_queue, LogParser(self.__input_queue.get()).parse())
