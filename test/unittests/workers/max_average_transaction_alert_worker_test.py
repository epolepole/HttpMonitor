import datetime
from queue import PriorityQueue

from mock import Mock

from workers.max_avg_transaction_worker import MaxAvgTransactionsAlertWorker


def test_alert_is_triggered():
    mocked_callback = Mock()
    today_epoch = int(datetime.datetime.now().timestamp())
    avg_stats = PriorityQueue()
    avg_stats.put((today_epoch + 0, 1 / 2))
    avg_stats.put((today_epoch + 1, 3 / 2))
    avg_stats.put((today_epoch + 2, 2))

    alert_worker = MaxAvgTransactionsAlertWorker(2, avg_stats, mocked_callback, 0.1)
    while not avg_stats.empty():
        alert_worker._iteration()
    iso_expected_time = datetime.datetime.fromtimestamp(today_epoch + 2).isoformat('T')
    mocked_callback.assert_called_once_with(
        "High traffic generated an alert - hits = {value}, triggered at {time}".format(value=2, time=iso_expected_time))


def test_alert_is_turned_off():
    mocked_callback = Mock()
    today_epoch = int(datetime.datetime.now().timestamp())
    avg_stats = PriorityQueue()
    avg_stats.put((today_epoch + 0, 1 / 2))
    avg_stats.put((today_epoch + 1, 3 / 2))
    avg_stats.put((today_epoch + 2, 2))
    avg_stats.put((today_epoch + 3, 3 / 2))
    alert_worker = MaxAvgTransactionsAlertWorker(2, avg_stats, mocked_callback, 0.1)
    while not avg_stats.empty():
        alert_worker._iteration()
    iso_expected_time = datetime.datetime.fromtimestamp(today_epoch + 3).isoformat('T')
    mocked_callback.assert_called_with("High traffic alert recovered at {time}".format(time=iso_expected_time))
