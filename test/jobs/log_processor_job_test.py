import datetime

from bom.average_stats import AverageStats
from bom.log import Log
from jobs.log_processor_job import LogProcessorJob


def test_process_average():
    bom_log_pq = [
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 50, 200)),
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 200)),
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 300)),
        Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 52, 400)),
    ]
    avg_stats = AverageStats(2)
    log_processor = LogProcessorJob(bom_log_pq, avg_stats)
    log_processor.loop(blocking=False)
    assert avg_stats.get() == (1 / 2, int(datetime.datetime(2018, 5, 9, 16, 0, 50).timestamp()))
    assert avg_stats.get() == (3 / 2, int(datetime.datetime(2018, 5, 9, 16, 0, 51).timestamp()))
