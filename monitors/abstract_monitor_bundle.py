import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class AbstractMonitorBundle:
    __metaclass__ = ABCMeta
    """
    A monitor bundle contains both the processor and the associated monitor that uses the output of the processor
    A future improvement would be to identify when a single processor can be used by several monitors, to avoid creating more than one of the same
    """

    @abstractmethod
    def get_worker(self, exception_queue):
        raise NotImplemented("This method should be overridden")

    @abstractmethod
    def get_processor(self):
        raise NotImplemented("This method should be overridden")
