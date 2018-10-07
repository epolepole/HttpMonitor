import logging
from queue import PriorityQueue, Queue

from bom.log_parser import LogParser
from jobs.abstract_job import AbstractJob

logger = logging.getLogger(__name__)


class LogFormatterJob(AbstractJob):
    def __init__(self, str_log_input_queue: Queue, bom_log_output_queue: PriorityQueue, interval):
        super().__init__(interval)
        self.__input_queue = str_log_input_queue
        self.__output_queue = bom_log_output_queue

    def _iteration(self):
        while not self.__input_queue.empty():
            # logger.debug("Parsing log")
            try:
                self.__output_queue.put(LogParser(self.__input_queue.get()).parse())
            except ValueError as ex:
                logger.warning(str(ex))
