import logging
import time
from queue import Empty, Queue

logger = logging.getLogger(__name__)


class HttpMonitor:
    def __init__(self, jobs_list, ex_bucket: Queue):
        self.__jobs = jobs_list
        self.__ex_bucket = ex_bucket

    def start_processes(self, blocking=True):
        self.__start()
        if blocking:
            self.__run()

    def __start(self):
        logger.debug("Starting start")
        for job in self.__jobs:
            job.start()

    def stop_processes(self):
        logger.debug("Calling stop")
        for job in self.__jobs:
            job.stop()
            job.join(3)

    def __run(self):
        while True:
            try:
                exc = self.__ex_bucket.get(block=False, timeout=0.1)
            except Empty:
                pass
            else:
                logger.error(str(exc))
                self.stop_processes()
                time.sleep(0.2)
                raise exc

            if self.__all_threads_alive():
                time.sleep(0.2)
                continue
            else:
                self.stop_processes()
                break

    def __all_threads_alive(self):
        for job in self.__jobs:
            if not job.isAlive():
                return False
        return True
