from collections import defaultdict
from queue import Queue


class AverageStats:
    def __init__(self, avg_time_frame, trx_max_seconds=None):
        self.trx_avg = Queue()
        self.__trx_avg_max_seconds = trx_max_seconds if trx_max_seconds else int(avg_time_frame * 1.2)
        self.__avg_time_frame = avg_time_frame
        self.__current_second = None
        self._trx_per_sec = defaultdict(int)

    def __generate_average(self, last_second):
        sum_cumulative = sum([self._trx_per_sec[last_second - delta] for delta in range(0, self.__avg_time_frame)])
        if last_second - self.__avg_time_frame + 1 in self._trx_per_sec:
            del self._trx_per_sec[last_second - self.__avg_time_frame + 1]
        self.trx_avg.put(sum_cumulative / self.__avg_time_frame)

    def increment_trx_at(self, second):
        self._trx_per_sec[second] += 1
        if not self.__current_second:
            self.__current_second = second
        if second > self.__current_second:
            self.__generate_average(self.__current_second)
            self.__current_second = second
