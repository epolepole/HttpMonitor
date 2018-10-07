import logging
import time
from queue import PriorityQueue

from bom.log import Log
from common import logger_configuration
from processors.basic_stats_processor import BasicStatsProcessor

logger_configuration.configure_logging(log_to_stdout=True, is_debug=True)
logger = logging.getLogger(__name__)


def add_logs(basic_stats_processor: BasicStatsProcessor):
    basic_stats_processor.process_log(Log(user_id="mike", method="get", resource="/api", status_code="200"))
    basic_stats_processor.process_log(Log(user_id="mike", method="get", resource="/tools", status_code="200"))
    basic_stats_processor.process_log(Log(user_id="john", method="post", resource="/api", status_code="201"))
    basic_stats_processor.process_log(Log(user_id="mike", method="post", resource="/api", status_code="500"))


def test_basic_stats_are_calculated():
    basic_stats_queue = PriorityQueue()
    basic_stats_processor = BasicStatsProcessor(basic_stats_queue, 0.2)
    add_logs(basic_stats_processor)
    time.sleep(0.30)
    add_logs(basic_stats_processor)

    basic_stats = basic_stats_queue.get(block=False)
    assert basic_stats.trx_per_sec == 20.
    assert basic_stats.trx_per_resource == {"/api": 3, "/tools": 1}
    assert basic_stats.trx_per_user == {"mike": 3, "john": 1}
    assert basic_stats.trx_per_method == {"get": 2, "post": 2}
    assert basic_stats.trx_per_status == {"200": 2, "201": 1, "500": 1}
