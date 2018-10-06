import time
from abc import ABCMeta, abstractmethod


class AbstractJob:
    __metaclass__ = ABCMeta

    def __init__(self, interval=0.5):
        self.__interval = interval
        self.__running = False

    def setup(self):
        pass

    def tear_down(self):
        pass

    @abstractmethod
    def _iteration(self):
        raise NotImplemented("This method should be overridden")

    def loop(self, blocking=True):
        self.__running = True
        while self.__running:
            self._iteration()
            if not blocking:
                return
            time.sleep(self.__interval)

    def stop(self):
        self.__running = False
