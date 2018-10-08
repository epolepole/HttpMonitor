import logging
from abc import ABCMeta, abstractmethod
from queue import Queue

logger = logging.getLogger(__name__)


class AbstractMonitorBundle:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_job(self, ex_queue):
        raise NotImplemented("This method should be overridden")

    @abstractmethod
    def get_processor(self):
        raise NotImplemented("This method should be overridden")
