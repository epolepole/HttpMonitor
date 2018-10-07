from bom.average_stats import AverageStats
from jobs.abstract_job import AbstractJob


class MaxAvgTransactionsAlert(AbstractJob):
    alarm_active_text = "High traffic generated an alert - hits = {value}, triggered at {time}"
    alarm_recovered_text = "High traffic generated alert recovered at {time}"

    def __init__(self, threshold, average_stats_queue: AverageStats, callback, interval=0.8):
        super().__init__(interval)
        self.__avg_stats_queue = average_stats_queue
        self.__callback = callback
        self.__threshold = threshold
        self.__is_active = False

    def _iteration(self):
        while not self.__avg_stats_queue.empty():
            avg, time = self.__avg_stats_queue.get()
            if not self.__is_active and avg >= self.__threshold:
                self.__is_active = True
                self.__callback(MaxAvgTransactionsAlert.alarm_active_text.format(value=int(avg), time=time))
            elif self.__is_active and avg < self.__threshold:
                self.__callback(MaxAvgTransactionsAlert.alarm_recovered_text.format(time=time))
