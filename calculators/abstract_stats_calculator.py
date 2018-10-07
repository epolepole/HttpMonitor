from abc import abstractmethod

from bom.log import Log


class AbstractStatsCalculator:
    @abstractmethod
    def process_log(self, log: Log):
        raise NotImplemented("This method should be overridden")
