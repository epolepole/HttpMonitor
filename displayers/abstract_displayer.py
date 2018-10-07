from abc import ABCMeta, abstractmethod


class AbstractDisplayer:
    class ClassWithLoop:
        __metaclass__ = ABCMeta

    @abstractmethod
    def display(self, data):
        raise NotImplemented("This method should be overridden")
