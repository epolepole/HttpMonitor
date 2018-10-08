import datetime
import logging
from queue import PriorityQueue, Queue

from jobs.abstract_job import AbstractJob

logger = logging.getLogger(__name__)


class MaxAvgTransactionsAlert(AbstractJob):
    alarm_active_text = "High traffic generated an alert - hits = {value}, triggered at {time}"
    alarm_recovered_text = "High traffic alert recovered at {time}"

    def __init__(self, threshold, average_stats_pqueue: PriorityQueue, callback, interval, ex_queue=Queue()):
        super().__init__(interval, ex_queue)
        self.__avg_stats_pqueue = average_stats_pqueue
        self.__callback = callback
        self.__threshold = threshold
        self.__is_active = False

    def _iteration(self):
        time, avg = self.__avg_stats_pqueue.get(timeout=self._queue_timeout)
        iso_time = datetime.datetime.fromtimestamp(time).isoformat('T')
        logger.debug("Checking average of {} for time {}".format(avg, iso_time))
        if not self.__is_active and avg >= self.__threshold:
            self.__is_active = True
            logger.info(MaxAvgTransactionsAlert.alarm_active_text.format(value=int(avg), time=iso_time))
            self.__callback(MaxAvgTransactionsAlert.alarm_active_text.format(value=int(avg), time=iso_time))
        elif self.__is_active and avg < self.__threshold:
            self.__is_active = False
            logger.info(MaxAvgTransactionsAlert.alarm_recovered_text.format(time=iso_time))
            self.__callback(MaxAvgTransactionsAlert.alarm_recovered_text.format(time=iso_time))
