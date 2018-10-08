from queue import PriorityQueue, Queue

from bom.basic_stats import BasicStats
from jobs.abstract_job import AbstractJob


class BasicStatsJob(AbstractJob):
    def __init__(self, basic_info_queue: PriorityQueue, callback, interval, ex_queue=Queue()):
        super().__init__(interval, ex_queue)
        self.__callback = callback
        self.__basic_info_pqueue = basic_info_queue
        self.__stats_to_print = dict()

    def __aggreagate_status_codes(self, codes):
        aggregated_codes = {
            "2xx": 0,
            "3xx": 0,
            "4xx": 0,
            "5xx": 0
        }
        for code, hits in codes.items():
            if code[0] == "2":
                aggregated_codes["2xx"] += hits
            elif code[0] == "3":
                aggregated_codes["3xx"] += hits
            elif code[0] == "4":
                aggregated_codes["4xx"] += hits
            elif code[0] == "5":
                aggregated_codes["5xx"] += hits
        return aggregated_codes

    def _process_stat(self, basic_stats: BasicStats):
        to_return = dict()
        to_return["time"] = basic_stats.timestamp.isoformat('T')
        to_return["transactions_per_second"] = basic_stats.trx_per_sec
        to_return["most_hits"] = list([k for k in sorted(basic_stats.trx_per_resource, key=basic_stats.trx_per_resource.get, reverse=True)])[0:3]
        to_return["most_active_users"] = list([k for k in sorted(basic_stats.trx_per_user, key=basic_stats.trx_per_user.get, reverse=True)])[0:3]
        to_return["status_codes"] = self.__aggreagate_status_codes(basic_stats.trx_per_status)
        self.__callback(to_return)

    def _iteration(self):
        self._process_stat(self.__basic_info_pqueue.get(timeout=self._queue_timeout))
