from abc import abstractmethod

from common.bom.log import Log


class AbstractStatsProcessor:
    @abstractmethod
    def process_log(self, log: Log):
        raise NotImplemented("This method should be overridden")
