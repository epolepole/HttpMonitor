import logging
import threading
import time
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class AbstractJob(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, interval=0.5):
        super().__init__()
        self.__interval = interval
        self.__running = False

    def setup(self):
        pass

    def tear_down(self):
        pass

    @abstractmethod
    def _iteration(self):
        raise NotImplemented("This method should be overridden")

    def run(self):
        logger.debug("Starting {} job".format(type(self).__name__))
        self.setup()
        self.loop()

    def loop(self, blocking=True):
        self.__running = True
        while self.__running:
            self._iteration()
            if not blocking:
                return
            time.sleep(self.__interval)

    def stop(self):
        logger.debug("Stopping {} job".format(type(self).__name__))
        self.__running = False
        time.sleep(self.__interval + 0.1)
        self.tear_down()
