import datetime
from queue import PriorityQueue

from mock import Mock

from bom.basic_stats import BasicStats
from monitors.monitor_jobs.basic_stats_job import BasicStatsJob


def test_basic_info_is_sent_to_the_callback():
    mocked_callback = Mock()

    basic_info = PriorityQueue()
    now = datetime.datetime.now()
    basic_stats_1 = BasicStats()
    basic_stats_1.timestamp = now
    basic_stats_1.trx_per_sec = 15
    basic_stats_1.trx_per_resource = {"/path_a": 1, "/path_b": 2, "/path_c": 3, "/path_d": 4}
    basic_stats_1.trx_per_user = {"user_a": 1, "user_b": 3, "user_c": 3, "user_d": 3}
    basic_stats_1.trx_per_method = {"get": 2, "post": 1, "put": 4, "delete": 3}
    basic_stats_1.trx_per_status = {"200": 4, "201": 1, "500": 3, "404": 2}

    basic_info.put(basic_stats_1)

    basic_stats_job = BasicStatsJob(basic_info, mocked_callback, 0.1)
    basic_stats_job.loop(blocking=False)

    expected_output = {
        "time":              now.isoformat('T'),
        "tps":               15,
        "most_hits":         ["/path_d", "/path_c", "/path_b"],
        "most_active_users": ["user_b", "user_c", "user_d"],
        "status_codes":      {"2xx": 5, "3xx": 0, "4xx": 2, "5xx": 3}
    }
    mocked_callback.assert_called_once_with(expected_output)
