from queue import Queue

from bom.jobs_intervals import JobsIntervals
from http_monitor import HttpMonitor
from jobs.file_reader_job import FileReaderJob
from jobs.log_formatter_job import LogFormatterJob
from jobs.log_processor_job import LogProcessorJob


class HttpMonitorBuilder(object):
    def __init__(self, log_file_path, intervals=JobsIntervals()):
        self._log_file_path = log_file_path
        self.__intervals = intervals
        self.__jobs = []
        # Creating the shared items between jobs
        self.__str_job_queue = Queue()
        self.__bom_log_pqueue = []
        self.__stats_calculators = list()

        self.__init_jobs()

    def __init_jobs(self):
        self.__jobs.append(FileReaderJob(self._log_file_path, self.__str_job_queue, self.__intervals.file_reader))
        self.__jobs.append(LogFormatterJob(self.__str_job_queue, self.__bom_log_pqueue, self.__intervals.log_formatter))
        self.__jobs.append(LogProcessorJob(self.__bom_log_pqueue, self.__stats_calculators, self.__intervals.log_processor))

    def add_monitor(self, monitor_bundle):
        self.__stats_calculators.append(monitor_bundle.calculator)
        self.__jobs.append(monitor_bundle.job)

    def get_monitor(self):
        return HttpMonitor(self.__jobs)
