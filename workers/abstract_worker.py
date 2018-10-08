import logging
import threading
import time
from abc import ABCMeta, abstractmethod
from queue import Empty

logger = logging.getLogger(__name__)


class AbstractWorker(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, interval, exception_queue):
        super().__init__()
        self.__interval = interval
        self.__exception_queue = exception_queue
        self.__running = False
        self._queue_timeout = 0.05

    def loop(self):
        self.__running = True
        while self.__running:
            try:
                self._iteration()
            except Empty:
                pass
            time.sleep(self.__interval)

    @abstractmethod
    def _iteration(self):
        raise NotImplemented("This method should be overridden")

    def run(self):
        logger.debug("Starting {} worker".format(type(self).__name__))
        try:
            self.setup()
            self.loop()
        except Exception as ex:
            logger.error(str(ex))
            self.__exception_queue.put(ex)
        finally:
            self.stop()

    def setup(self):
        pass

    def tear_down(self):
        pass

    def stop(self):
        if self.__running:
            logger.debug("Stopping {} worker".format(type(self).__name__))
            self.__running = False
            time.sleep(self.__interval + 0.1)
            self.tear_down()
