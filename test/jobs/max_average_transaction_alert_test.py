from mock import Mock

from bom.average_stats import AverageStats
from jobs.abstract_job import AbstractJob


class MaxTransactionsAlert(AbstractJob):
    alarm_active_text = "High traffic generated an alert - hits = {value}, triggered at {time}"
    alarm_recovered_text = "High traffic generated alert recovered at {time}"

    def __init__(self, time_frame, threshold, average_stats_queue: AverageStats, callback, interval=0.8):
        super().__init__(interval)
        self.__avg_stats_queue = average_stats_queue
        self.__callback = callback
        self.__time_frame = time_frame
        self.__threshold = threshold
        self.__is_active = False

    def _iteration(self):
        while not self.__avg_stats_queue.empty():
            avg, time = self.__avg_stats_queue.get()
            if not self.__is_active and avg >= self.__threshold:
                self.__is_active = True
                self.__callback(MaxTransactionsAlert.alarm_active_text.format(value=int(avg), time=time))
            elif self.__is_active and avg < self.__threshold:
                self.__callback(MaxTransactionsAlert.alarm_recovered_text.format(time=time))


def test_alert_is_triggered():
    mocked_callback = Mock()
    avg_stats = AverageStats(2)
    alert_job = MaxTransactionsAlert(2, 2, avg_stats, mocked_callback)
    avg_stats.increment_trx_at(24)
    avg_stats.increment_trx_at(25)
    avg_stats.increment_trx_at(25)
    avg_stats.increment_trx_at(26)
    avg_stats.increment_trx_at(26)
    avg_stats.increment_trx_at(27)
    alert_job.loop(blocking=False)
    mocked_callback.assert_called_once_with("High traffic generated an alert - hits = {value}, triggered at {time}".format(value=2, time=26))


def test_alert_is_turned_off():
    mocked_callback = Mock()
    avg_stats = AverageStats(2)
    alert_job = MaxTransactionsAlert(2, 2, avg_stats, mocked_callback)
    avg_stats.increment_trx_at(24)
    avg_stats.increment_trx_at(25)
    avg_stats.increment_trx_at(25)
    avg_stats.increment_trx_at(26)
    avg_stats.increment_trx_at(26)
    avg_stats.increment_trx_at(27)
    avg_stats.increment_trx_at(28)
    alert_job.loop(blocking=False)
    mocked_callback.assert_called_with("High traffic generated alert recovered at {time}".format(time=27))
