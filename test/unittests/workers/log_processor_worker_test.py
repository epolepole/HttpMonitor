import datetime
import logging
from queue import PriorityQueue

from common import logger_configuration
from common.bom.log import Log
from monitors.processors.avg_stats_processor import AvgStatsProcessor
from workers.log_processor_worker import LogProcessorWorker

logger_configuration.configure_logging(log_to_stdout=True, is_debug=True)
logger = logging.getLogger(__name__)


def test_process_average():
    bom_log_pq = PriorityQueue()
    bom_log_pq.put(Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 50, 200)))
    bom_log_pq.put(Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 200)))
    bom_log_pq.put(Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 51, 300)))
    bom_log_pq.put(Log(timestamp=datetime.datetime(2018, 5, 9, 16, 0, 52, 400)))
    time_period = 2
    avg_stats_pqueue = PriorityQueue()
    calculators = [AvgStatsProcessor(avg_stats_pqueue, time_period)]
    log_processor = LogProcessorWorker(bom_log_pq, calculators, 0.1)
    while not bom_log_pq.empty():
        log_processor._iteration()
    assert avg_stats_pqueue.get(timeout=0.5) == (int(datetime.datetime(2018, 5, 9, 16, 0, 50).timestamp()), 1 / 2)
    assert avg_stats_pqueue.get(timeout=0.5) == (int(datetime.datetime(2018, 5, 9, 16, 0, 51).timestamp()), 3 / 2)
