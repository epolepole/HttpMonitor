from mock import Mock

from bom.average_stats import AverageStats
from jobs.max_average_transaction_alert import MaxAvgTransactionsAlert


def test_alert_is_triggered():
    mocked_callback = Mock()
    avg_stats = AverageStats(2)
    alert_job = MaxAvgTransactionsAlert(2, 2, avg_stats, mocked_callback)
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
    alert_job = MaxAvgTransactionsAlert(2, 2, avg_stats, mocked_callback)
    avg_stats.increment_trx_at(24)
    avg_stats.increment_trx_at(25)
    avg_stats.increment_trx_at(25)
    avg_stats.increment_trx_at(26)
    avg_stats.increment_trx_at(26)
    avg_stats.increment_trx_at(27)
    avg_stats.increment_trx_at(28)
    alert_job.loop(blocking=False)
    mocked_callback.assert_called_with("High traffic generated alert recovered at {time}".format(time=27))
