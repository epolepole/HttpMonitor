from queue import Queue

from bom.log_builder import LogBuilder
from jobs.abstract_job import AbstractJob


class LogFormatterJob(AbstractJob):
    def __init__(self, str_log_input_queue: Queue, bom_log_output_queue: Queue, interval=0.01):
        super().__init__(interval)
        self.__input_queue = str_log_input_queue
        self.__output_queue = bom_log_output_queue

    def _iteration(self):
        self.__output_queue.put(LogBuilder(self.__input_queue.get()).get_log())
