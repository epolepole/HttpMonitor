import logging
import time
from queue import Empty, Queue

logger = logging.getLogger(__name__)


class HttpMonitor:
    def __init__(self, jobs_list, ex_bucket: Queue):
        self.__jobs = jobs_list
        self.__ex_bucket = ex_bucket

    def start(self, blocking=True):
        self.__start()
        if blocking:
            self.__blocking_loop()

    def stop(self):
        logger.debug("Calling exit")
        for job in self.__jobs:
            job.stop()
            job.join(0.01)

    def __start(self):
        logger.debug("Starting enter")
        for job in self.__jobs:
            job.start()

    def __blocking_loop(self):
        while True:
            try:
                exc = self.__ex_bucket.get(block=False, timeout=0.1)
            except Empty:
                pass
            else:
                logger.error(str(exc))
                self.stop()
                time.sleep(0.2)
                raise exc

            if self.__is_alive():
                continue
            else:
                break

    def __is_alive(self):
        for job in self.__jobs:
            if not job.isAlive():
                return False
        return True
