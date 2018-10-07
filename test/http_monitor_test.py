import logging
import time

from common import logger_configuration
from http_monitor import HttpMonitor
from jobs.abstract_job import AbstractJob

logger_configuration.configure_logging("http_monitor_test.log", is_debug=True)
logger = logging.getLogger(__name__)


class TestJob(AbstractJob):
    def __init__(self, text):
        super().__init__(0.1)
        self.__text = text

    def _iteration(self):
        logger.debug(self.__text)


def test_http_monitor_calls_jobs():
    jobs = [
        TestJob("Job A"),
        TestJob("Job B"),
        TestJob("Job C")
    ]
    with HttpMonitor(jobs):
        time.sleep(2)
