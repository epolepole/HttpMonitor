import datetime
import re

from bom.log import Log

# '127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 1234'
"""
127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326

    A "-" in a field indicates missing data.

    127.0.0.1 is the IP address of the client (remote host) which made the request to the server.
    user-identifier is the RFC 1413 identity of the client.
    frank is the userid of the person requesting the document.
    [10/Oct/2000:13:55:36 -0700] is the date, time, and time zone that the request was received, by default in strftime format %d/%b/%Y:%H:%M:%S %z.
    "GET /apache_pb.gif HTTP/1.0" is the request line from the client. The method GET, /apache_pb.gif the resource requested, and HTTP/1.0 the HTTP protocol.
    200 is the HTTP status code returned to the client. 2xx is a successful response, 3xx a redirection, 4xx a client error, and 5xx a server error.
    2326 is the size of the object returned to the client, measured in bytes.
"""

LOG_TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


class LogParser:
    section_re_compiled = re.compile(r'([(\d.)]+) (.*?) (.*?) \[(.*?)\] "(.*?) (.*?) (.*?)" (\d+) (\d+)')

    def __init__(self, log_str: str):
        self.__str = log_str
        self.__log = Log()
        self.__m = None

    def __parse_internal(self):
        self.__m = LogParser.section_re_compiled.match(self.__str)
        if not self.__m or len(self.__m.groups()) != 9:
            raise ValueError("Wrong log format for {}".format(self.__str))

        self.__log.client_ip = self.__match_or_none(0)
        self.__log.user_identifier = self.__match_or_none(1)
        self.__log.user_id = self.__match_or_none(2)
        self.__log.timestamp = self.__get_time_stamp(3)
        self.__log.method = self.__match_or_none(4)
        self.__log.resource = self.__match_or_none(5)
        self.__log.protocol = self.__match_or_none(6)
        self.__log.status_code = self.__match_or_none(7)
        self.__log.response_size = self.__match_or_none(8)

    def __get_time_stamp(self, idx):
        time_str = self.__match_or_none(idx)
        if time_str is None:
            return None
        return datetime.datetime.strptime(time_str, LOG_TIMESTAMP_FORMAT)

    def __match_or_none(self, idx):
        return self.__m.groups()[idx] if self.__m.groups()[idx] != '-' else None

    def parse(self):
        self.__parse_internal()
        return self.__log
