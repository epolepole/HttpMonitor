import datetime
from queue import PriorityQueue

from common.bom.log import Log
from monitors.processors.avg_stats_processor import AvgStatsProcessor


def test_average_is_calculated():
    avg_stats = PriorityQueue()
    average_stats_processor = AvgStatsProcessor(avg_stats, 3)
    today_epoch = int(datetime.datetime.now().timestamp())

    average_stats_processor.process_log(Log(timestamp=datetime.datetime.fromtimestamp(today_epoch)))
    average_stats_processor.process_log(Log(timestamp=datetime.datetime.fromtimestamp(today_epoch)))
    average_stats_processor.process_log(Log(timestamp=datetime.datetime.fromtimestamp(today_epoch + 1)))
    assert avg_stats.get() == (today_epoch, 2 / 3)

    average_stats_processor.process_log(Log(timestamp=datetime.datetime.fromtimestamp(today_epoch + 2)))
    assert avg_stats.get() == (today_epoch + 1, 1)
