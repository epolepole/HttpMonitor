class Log:
    def __init__(self):
        self.section = None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
