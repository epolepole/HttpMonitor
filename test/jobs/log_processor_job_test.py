import datetime

from bom.log import Log
from bom.stats_container import StatsContainer
from jobs.log_processor_job import LogProcessorJob


def test_process_average():
    bom_log_pq = [
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 50, 200)),
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 200)),
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 300)),
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 52, 400)),
    ]
    stats_container = StatsContainer()
    time_period = 2
    stats_container.add_avg_stats(time_period)
    log_processor = LogProcessorJob(bom_log_pq, stats_container, 0.1)
    log_processor.loop(blocking=False)
    assert stats_container.get_avg_stats(time_period).get() == (1 / 2, int(datetime.datetime(2018, 5, 9, 16, 0, 50).timestamp()))
    assert stats_container.get_avg_stats(time_period).get() == (3 / 2, int(datetime.datetime(2018, 5, 9, 16, 0, 51).timestamp()))
