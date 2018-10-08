import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class AbstractMonitorBundle:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_worker(self, exception_queue):
        raise NotImplemented("This method should be overridden")

    @abstractmethod
    def get_processor(self):
        raise NotImplemented("This method should be overridden")
