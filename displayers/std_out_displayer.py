import json

from displayers.abstract_displayer import AbstractDisplayer


class StdOutAbstractDisplayer(AbstractDisplayer):
    def display(self, data):
        print(json.dumps(data))
