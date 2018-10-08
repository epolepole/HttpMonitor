import logging
import time
from queue import Empty, Queue

logger = logging.getLogger(__name__)


class HttpMonitor:
    """
    Class to handle and orchestrate the workers execution.
    It also handles the exceptions inside workers thanks to the exception bucket
    """

    def __init__(self, workers_list, exception_bucket: Queue):
        self.__workers = workers_list
        self.__exception_bucket = exception_bucket

    def start_workers(self, blocking=True):
        """

        :param blocking: If set to false, no exception handling will be supported and the call will be non blocking.
        Stop method will need to be called afterwards
        """
        self.__start()
        if blocking:
            self.__run()

    def __start(self):
        logger.debug("Starting start")
        for worker in self.__workers:
            worker.start()

    def stop_workers(self):
        logger.debug("Calling stop")
        for worker in self.__workers:
            worker.stop()
            worker.join(3)

    def __run(self):
        while True:
            try:
                exc = self.__exception_bucket.get(block=False, timeout=0.1)
            except Empty:
                """If the exception bucket is empty we continue in the loop"""
                pass
            else:
                """If there is an exception in the bucket, we log it, stop the workers and rerise the exception"""
                logger.error(str(exc))
                self.stop_workers()
                time.sleep(0.2)
                raise exc

            if self.__all_threads_alive():
                """Ensure all threads are alive, otherwise stop the process"""
                time.sleep(0.2)
                continue
            else:
                self.stop_workers()
                break

    def __all_threads_alive(self):
        for worker in self.__workers:
            if not worker.isAlive():
                return False
        return True
