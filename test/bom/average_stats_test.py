from collections import defaultdict
from queue import Queue


class AverageStats:
    def __init__(self, avg_time_frame, trx_max_seconds=None):
        self.trx_avg_max_seconds = trx_max_seconds if trx_max_seconds else int(avg_time_frame * 1.2)
        self.avg_time_frame = avg_time_frame
        self.trx_avg = Queue()
        self.current_second = None
        self.trx_per_sec = defaultdict(int)

    def generate_average(self, last_second):
        sum_cumulative = sum([self.trx_per_sec[last_second - delta] for delta in range(0, self.avg_time_frame)])
        if last_second - self.avg_time_frame + 1 in self.trx_per_sec:
            del self.trx_per_sec[last_second - self.avg_time_frame + 1]
        self.trx_avg.put(sum_cumulative / self.avg_time_frame)

    def add_trx(self, second):
        self.trx_per_sec[second] += 1
        if not self.current_second:
            self.current_second = second
        if second > self.current_second:
            self.generate_average(self.current_second)
            self.current_second = second


def test_average_is_calculated():
    average_stats = AverageStats(3)
    average_stats.add_trx(24)
    average_stats.add_trx(24)
    average_stats.add_trx(25)
    assert average_stats.trx_avg.get() == 2 / 3
    average_stats.add_trx(26)
    assert average_stats.trx_avg.get() == 1
    assert average_stats.trx_avg.empty() is True


def test_trx_is_cleaned():
    average_stats = AverageStats(3)
    average_stats.add_trx(24)
    average_stats.add_trx(24)
    average_stats.add_trx(25)
    average_stats.add_trx(26)
    average_stats.add_trx(27)
    average_stats.add_trx(28)
    assert 24 not in average_stats.trx_per_sec
    assert 25 not in average_stats.trx_per_sec
