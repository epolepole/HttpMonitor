import datetime
import heapq

from bom.log import Log
from processors.avg_stats_processor import AvgStatsProcessor


def test_average_is_calculated():
    avg_stats = []
    average_stats_processor = AvgStatsProcessor(avg_stats, 3)
    today_epoch = int(datetime.datetime.now().timestamp())

    average_stats_processor.process_log(Log(timestamp=datetime.datetime.fromtimestamp(today_epoch)))
    average_stats_processor.process_log(Log(timestamp=datetime.datetime.fromtimestamp(today_epoch)))
    average_stats_processor.process_log(Log(timestamp=datetime.datetime.fromtimestamp(today_epoch + 1)))
    assert heapq.heappop(avg_stats) == (today_epoch, 2 / 3)

    average_stats_processor.process_log(Log(timestamp=datetime.datetime.fromtimestamp(today_epoch + 2)))
    assert heapq.heappop(avg_stats) == (today_epoch + 1, 1)
