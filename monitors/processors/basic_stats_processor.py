import copy
import datetime
import logging
from queue import PriorityQueue

from bom.basic_stats import BasicStats
from bom.log import Log
from monitors.processors.abstract_stats_processor import AbstractStatsProcessor

logger = logging.getLogger(__name__)


class BasicStatsProcessor(AbstractStatsProcessor):
    def __init__(self, basic_stats_pqueue: PriorityQueue, time_period):
        self.__basic_stats_pqueue = basic_stats_pqueue
        self.__time_period = time_period
        self.__current_time = datetime.datetime.now()
        self.__aggregated_data = BasicStats()
        self.__aggregated_data.reset(self.__current_time)

    def process_log(self, log: Log):
        self.__put_if_period_passed()
        self.__aggregated_data.trx_per_resource[log.resource] += 1
        self.__aggregated_data.trx_per_user[log.user_id] += 1
        self.__aggregated_data.trx_per_method[log.method] += 1
        self.__aggregated_data.trx_per_status[log.status_code] += 1
        self.__aggregated_data.trx_per_sec += 1.0 / self.__time_period

    def __put_if_period_passed(self):
        now = datetime.datetime.now()
        if now - self.__current_time > datetime.timedelta(seconds=self.__time_period):
            logger.debug("Pushing basic stats")
            self.__current_time = now
            self.__basic_stats_pqueue.put(copy.deepcopy(self.__aggregated_data))
            self.__aggregated_data.reset(self.__current_time)
