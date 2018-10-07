from mock import Mock

from jobs.abstract_job import AbstractJob


class BasicStatsJob(AbstractJob):
    def __init__(self, callback, interval):
        super().__init__(interval)
        self.__callback = callback

    def _iteration(self):
        self.__callback("")


def test_basic_info_is_sent_to_the_callback():
    mocked_callback = Mock()
    basic_stats_job = BasicStatsJob(mocked_callback, 0.5)
