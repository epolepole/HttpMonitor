import logging
from collections.__init__ import defaultdict
from queue import PriorityQueue

from bom.log import Log
from monitors.processors.abstract_stats_processor import AbstractStatsProcessor

logger = logging.getLogger(__name__)


class AvgStatsProcessor(AbstractStatsProcessor):
    def __init__(self, average_stats_pqueue: PriorityQueue, time_period):
        self.__avg_stats_queue = average_stats_pqueue
        self.__time_period = time_period

        self.__trx_per_sec = defaultdict(int)
        self.__current_second = None

    def process_log(self, log: Log):
        self.__increment_trx_at(log.second)

    def __generate_average(self, last_second):
        sum_cumulative = sum([self.__trx_per_sec[last_second - delta] for delta in range(0, self.__time_period)])
        if last_second - self.__time_period + 1 in self.__trx_per_sec:
            del self.__trx_per_sec[last_second - self.__time_period + 1]
        self.__avg_stats_queue.put((last_second, sum_cumulative / self.__time_period))

    def __increment_trx_at(self, second):
        self.__trx_per_sec[second] += 1
        if not self.__current_second:
            self.__current_second = second
        if second > self.__current_second:
            self.__generate_average(self.__current_second)
            self.__current_second = second
