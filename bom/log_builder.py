import re

from bom.log import Log


class LogBuilder:
    section_re_compiled = re.compile(r'.*?"[^/]*/([\w]*).*?".*?')

    def __init__(self, log_str: str):
        self.__str = log_str
        self.__section = None
        self.__log = Log()

    def __parse_section(self):
        m = LogBuilder.section_re_compiled.match(self.__str)
        if not m:
            raise ValueError("Section not found in {}".format(self.__str))
        self.__log.section = m.groups()[0]

    def get_log(self):
        self.__parse_section()
        return self.__log
