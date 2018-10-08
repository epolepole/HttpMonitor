from queue import PriorityQueue, Queue

from common.bom.workers_intervals import WorkersIntervals
from http_monitor import HttpMonitor
from workers.file_reader_worker import FileReaderWorker
from workers.log_formatter_worker import LogFormatterWorker
from workers.log_processor_worker import LogProcessorWorker


class HttpMonitorBuilder(object):
    def __init__(self, log_file_path, intervals=WorkersIntervals()):
        self._log_file_path = log_file_path
        self.__intervals = intervals
        self.__workers = []
        # Creating the shared items between workers
        self.__exception_queue = Queue()
        self.__str_log_queue = Queue()
        self.__bom_log_pqueue = PriorityQueue()
        self.__stats_processors = list()

        self.__init_workers()

    def __init_workers(self):
        """Initialize the Basic workers and add the correspondent shared queues and the shared exception queue"""
        self.__workers.append(FileReaderWorker(self._log_file_path, self.__str_log_queue, self.__intervals.file_reader, self.__exception_queue))
        self.__workers.append(
            LogFormatterWorker(self.__str_log_queue, self.__bom_log_pqueue, self.__intervals.log_formatter, self.__exception_queue))
        self.__workers.append(
            LogProcessorWorker(self.__bom_log_pqueue, self.__stats_processors, self.__intervals.log_processor, self.__exception_queue))

    def add_monitor(self, monitor_bundle):
        """Initialize the monitors and add the processors tu the processor worker"""
        self.__stats_processors.append(monitor_bundle.get_processor())
        self.__workers.append(monitor_bundle.get_worker(self.__exception_queue))

    def get_monitor(self):
        return HttpMonitor(self.__workers, self.__exception_queue)

    def get_ex_bucket(self):
        return self.__exception_queue
