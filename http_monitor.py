import logging
import threading
from asyncio import Queue

logger = logging.getLogger(__name__)


class ExceptinThread(threading.Thread):
    def __init__(self, jobs, ex_queue: Queue):
        self.__jobs = jobs
        self.__ex_queue = ex_queue

    def run(self):
        for job in self.__jobs:
            job.start()


class HttpMonitor:
    def __init__(self, jobs_list, ex_queue: Queue):
        self.__jobs = jobs_list
        self.__ex_queue = ex_queue

    def __start(self):
        for job in self.__jobs:
            job.start()

    def __stop(self):
        for job in self.__jobs:
            job.stop()
            job.join()

    def __enter__(self):
        logger.debug("Calling enter")
        self.__start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Calling exit")
        self.__stop()
