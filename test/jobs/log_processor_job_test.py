import datetime
from queue import PriorityQueue

from bom.log import Log
from jobs.log_processor_job import LogProcessorJob
from processors.avg_stats_processor import AvgStatsProcessor


def test_process_average():
    bom_log_pq = PriorityQueue()
    bom_log_pq.put(Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 50, 200)))
    bom_log_pq.put(Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 200)))
    bom_log_pq.put(Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 300)))
    bom_log_pq.put(Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 52, 400)))
    time_period = 2
    avg_stats_pqueue = PriorityQueue()
    calculators = [AvgStatsProcessor(avg_stats_pqueue, time_period)]
    log_processor = LogProcessorJob(bom_log_pq, calculators, 0.1)
    log_processor.loop(blocking=False)
    assert avg_stats_pqueue.get() == (int(datetime.datetime(2018, 5, 9, 16, 0, 50).timestamp()), 1 / 2)
    assert avg_stats_pqueue.get() == (int(datetime.datetime(2018, 5, 9, 16, 0, 51).timestamp()), 3 / 2)
