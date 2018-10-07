import logging
from abc import ABCMeta

logger = logging.getLogger(__name__)


class AbstractMonitorBundle:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.processor = None
        self.job = None
