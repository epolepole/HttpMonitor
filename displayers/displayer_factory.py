from enum import Enum

from displayers.file_displayer import FileAbstractDisplayer
from displayers.log_displayer import LogAbstractDisplayer
from displayers.std_out_displayer import StdOutAbstractDisplayer


class Displayers(Enum):
    LOG = 'log'
    FILE = 'file'
    STDOUT = 'stdout'

    def __str__(self):
        return self.value


class DisplayerFactory:
    @staticmethod
    def manufacture_displayer(type: Displayers, params=None):
        if type == Displayers.LOG:
            return LogAbstractDisplayer()
        elif type == Displayers.FILE:
            if params is None:
                raise ValueError("Expecting file path to create file displayer")
            return FileAbstractDisplayer(params)
        elif type == Displayers.STDOUT:
            return StdOutAbstractDisplayer()
        else:
            raise ValueError("Unknown displayer type")
