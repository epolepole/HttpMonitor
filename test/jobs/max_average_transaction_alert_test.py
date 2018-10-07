import datetime

from mock import Mock

from bom.average_stats import AverageStats
from jobs.max_avg_transaction_alert import MaxAvgTransactionsAlert


def test_alert_is_triggered():
    mocked_callback = Mock()
    avg_stats = AverageStats(2)
    alert_job = MaxAvgTransactionsAlert(2, avg_stats, mocked_callback, 0.1)
    today_epoch = int(datetime.datetime.now().timestamp())
    avg_stats.increment_trx_at(today_epoch + 0)
    avg_stats.increment_trx_at(today_epoch + 1)
    avg_stats.increment_trx_at(today_epoch + 1)
    avg_stats.increment_trx_at(today_epoch + 2)
    avg_stats.increment_trx_at(today_epoch + 2)
    avg_stats.increment_trx_at(today_epoch + 3)
    alert_job.loop(blocking=False)
    iso_expected_time = datetime.datetime.fromtimestamp(today_epoch + 2).isoformat('T')
    mocked_callback.assert_called_once_with(
        "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=2, time=iso_expected_time))


def test_alert_is_turned_off():
    mocked_callback = Mock()
    avg_stats = AverageStats(2)
    alert_job = MaxAvgTransactionsAlert(2, avg_stats, mocked_callback, 0.1)
    today_epoch = int(datetime.datetime.now().timestamp())
    avg_stats.increment_trx_at(today_epoch + 0)
    avg_stats.increment_trx_at(today_epoch + 1)
    avg_stats.increment_trx_at(today_epoch + 1)
    avg_stats.increment_trx_at(today_epoch + 2)
    avg_stats.increment_trx_at(today_epoch + 2)
    avg_stats.increment_trx_at(today_epoch + 3)
    avg_stats.increment_trx_at(today_epoch + 4)
    alert_job.loop(blocking=False)
    iso_expected_time = datetime.datetime.fromtimestamp(today_epoch + 3).isoformat('T')
    mocked_callback.assert_called_with("High traffic alert recovered at {time}".format(time=iso_expected_time))
