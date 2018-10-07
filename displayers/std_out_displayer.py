from displayers.abstract_displayer import AbstractDisplayer


class StdOutAbstractDisplayer(AbstractDisplayer):
    def display(self, data):
        print(str(data))
