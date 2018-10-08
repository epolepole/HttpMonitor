import logging
import os
from queue import Queue

from jobs.abstract_job import AbstractJob

logger = logging.getLogger(__name__)


class FileReaderJob(AbstractJob):
    def __init__(self, log_file_path, output_queue: Queue, interval, ex_queue=Queue()):
        super().__init__(interval, ex_queue)
        self.__file_path = os.path.realpath(log_file_path)
        self.__file = None
        self.__output_queue = output_queue

    def open_file(self):
        logger.debug("Opening file")
        try:
            self.__file = open(self.__file_path, 'r')
            self.__file.seek(os.path.getsize(self.__file_path))
            logger.debug("File {} opened to read".format(self.__file_path))
        except IOError as ex:
            logger.error('IO Exception when opening file {}. Exception: {}'.format(self.__file_path, str(ex)))
            raise ex

    def close_file(self):
        logger.debug("Closing file")
        if self.__file and not self.__file.closed:
            self.__file.close()
            logger.debug("File {} closed".format(self.__file_path))

    def setup(self):
        self.open_file()

    def tear_down(self):
        self.close_file()

    def _iteration(self):
        lines = self.__file.readlines()
        if len(lines) != 0:
            logger.debug("Calling callback with {}".format(str(lines)))
            for line in lines:
                self.__output_queue.put(line.strip('\n'))
