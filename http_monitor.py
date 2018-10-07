import logging

logger = logging.getLogger(__name__)


class HttpMonitor:
    def __init__(self, jobs_list):
        self.__jobs = jobs_list

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
