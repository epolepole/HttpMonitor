from bom.average_stats import AverageStats


def test_average_is_calculated():
    average_stats = AverageStats(3)
    average_stats.increment_trx_at(24)
    average_stats.increment_trx_at(24)
    average_stats.increment_trx_at(25)
    assert average_stats.trx_avg.get() == 2 / 3
    average_stats.increment_trx_at(26)
    assert average_stats.trx_avg.get() == 1
    assert average_stats.trx_avg.empty() is True


def test_trx_is_cleaned():
    average_stats = AverageStats(3)
    average_stats.increment_trx_at(24)
    average_stats.increment_trx_at(24)
    average_stats.increment_trx_at(25)
    average_stats.increment_trx_at(26)
    average_stats.increment_trx_at(27)
    average_stats.increment_trx_at(28)
    assert 24 not in average_stats._trx_per_sec
    assert 25 not in average_stats._trx_per_sec
