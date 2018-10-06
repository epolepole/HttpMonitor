from functools import total_ordering


@total_ordering
class Log:
    def __init__(self, client_ip=None, user_identifier=None, user_id=None, timestamp=None, method=None, resource=None, protocol=None,
                 status_code=None,
                 response_size=None):
        self.client_ip = client_ip
        self.user_identifier = user_identifier
        self.user_id = user_id
        self.timestamp = timestamp
        self.method = method
        self.resource = resource
        self.protocol = protocol
        self.status_code = status_code
        self.response_size = response_size

    @property
    def second(self):
        second_precision = self.timestamp
        return second_precision.replace(microsecond=0)

    def __str__(self):
        return str(self.__dict__)

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
