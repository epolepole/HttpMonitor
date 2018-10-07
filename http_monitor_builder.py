from queue import Queue

from bom.jobs_intervals import JobsIntervals
from bom.stats_container import StatsContainer
from http_monitor import HttpMonitor
from jobs.file_reader_job import FileReaderJob
from jobs.log_formatter_job import LogFormatterJob
from jobs.log_processor_job import LogProcessorJob
from jobs.max_avg_transaction_alert import MaxAvgTransactionsAlert


class HttpMonitorBuilder(object):
    def __init__(self, log_file_path, intervals=JobsIntervals()):
        self._log_file_path = log_file_path
        self.__intervals = intervals
        self.__jobs = []
        # Creating the shared items between jobs
        self.__str_job_queue = Queue()
        self.__bom_log_pqueue = []
        self.__stats_container = StatsContainer()

        self.__init_jobs()

    def __init_jobs(self):
        self.__jobs.append(FileReaderJob(self._log_file_path, self.__str_job_queue, self.__intervals.file_reader))
        self.__jobs.append(LogFormatterJob(self.__str_job_queue, self.__bom_log_pqueue, self.__intervals.log_formatter))
        self.__jobs.append(LogProcessorJob(self.__bom_log_pqueue, self.__stats_container, self.__intervals.log_processor))

    def add_avg_alert(self, time_period, threshold, callback, interval=0.1):
        self.__stats_container.add_avg_stats(time_period)
        self.__jobs.append(MaxAvgTransactionsAlert(threshold, self.__stats_container.get_avg_stats(time_period), callback, interval))

    def get_monitor(self):
        return HttpMonitor(self.__jobs)
