import logging
from queue import PriorityQueue, Queue

from workers.abstract_worker import AbstractWorker

logger = logging.getLogger(__name__)


class LogProcessorWorker(AbstractWorker):
    def __init__(self, input_queue: PriorityQueue, stats_processors: list, interval, exception_queue=Queue()):
        super().__init__(interval, exception_queue)
        self.__input_pq = input_queue
        self.__stats_processors = stats_processors

    def _iteration(self):
        log = self.__input_pq.get(timeout=self._queue_timeout)
        for calculator in self.__stats_processors:
            calculator.process_log(log)
