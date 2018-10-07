import heapq
import logging

from bom.stats_container import StatsContainer
from jobs.abstract_job import AbstractJob

logger = logging.getLogger(__name__)


class LogProcessorJob(AbstractJob):
    def __init__(self, input_queue: list, output_stats: StatsContainer, interval):
        super().__init__(interval)
        self.__input_pq = input_queue
        self.__output_stats = output_stats

    def _iteration(self):
        while len(self.__input_pq) != 0:
            # logger.debug("Processing log")
            log = heapq.heappop(self.__input_pq)
            for avg_stats in self.__output_stats.average_stats_dict.values():
                avg_stats.increment_trx_at(log.second)
