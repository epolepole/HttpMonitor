import logging
import threading
import time
from abc import ABCMeta, abstractmethod
from queue import Empty

logger = logging.getLogger(__name__)


class StoppingException(Exception):
    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return "Stopping exception from {}".format(self.__msg)


class AbstractJob(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, interval, exception_queue):
        super().__init__()
        self.__interval = interval
        self.__ex_queue = exception_queue
        self.__running = False
        self._queue_timeout = 0.05

    def setup(self):
        pass

    def tear_down(self):
        pass

    @abstractmethod
    def _iteration(self):
        raise NotImplemented("This method should be overridden")

    def run(self):
        logger.debug("Starting {} job".format(type(self).__name__))
        try:
            self.setup()
            self.loop()
        except Exception as ex:
            logger.error(str(ex))
            self.__ex_queue.put(ex)
        finally:
            self.stop()

    def loop(self, blocking=True):
        self.__running = True
        while self.__running:
            try:
                self._iteration()
            except Empty:
                pass
            if not blocking:
                return
            time.sleep(self.__interval)

    def stop(self):
        if self.__running:
            logger.debug("Stopping {} job".format(type(self).__name__))
            self.__running = False
            time.sleep(self.__interval + 0.1)
            self.tear_down()
