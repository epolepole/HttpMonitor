import json

from displayers.abstract_displayer import AbstractDisplayer


class FileAbstractDisplayer(AbstractDisplayer):
    def __init__(self, file_name):
        self.__file_name = file_name

    def display(self, data):
        with open(self.__file_name, 'a') as file:
            file.write("{}\n".format(json.dumps(data)))
