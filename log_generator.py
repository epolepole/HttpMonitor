#!/usr/bin/env python
import datetime
import random
import time
from http import HTTPStatus

import pytz as pytz

DEFAULT_LOG_FORMAT = '127.0.0.1 - {name} [{timestamp}] "{method} {path} HTTP/1.0" {status} 1234\n'
LOG_TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S +0000"

names = ["Mike", "Thom", "Alan", "Evelyn", "Clara", "Ane"]
methods = ["GET", "POST", "PUT", "DELETE"]
paths = ["/api", "/users", "/statistics", "/data"]


def write_line(log_file):
    name = random.choice(names)
    now = datetime.datetime.now(pytz.utc).strftime(LOG_TIMESTAMP_FORMAT)
    method = random.choice(methods)
    path = random.choice(paths)
    status = random.choice([http_code.value for http_code in HTTPStatus])
    log_file.write(DEFAULT_LOG_FORMAT.format(name=name, timestamp=now, method=method, path=path, status=status))
    log_file.flush()


if __name__ == "__main__":
    with open("logs/access.log", 'a') as log_file:
        old_time = datetime.datetime.now(pytz.utc)
        now = old_time
        print("Starting low traffic for 10 seconds")
        while now - old_time < datetime.timedelta(seconds=10):
            now = datetime.datetime.now(pytz.utc)
            time.sleep(0.3)
            write_line(log_file)
        print("Starting high traffic for 5 seconds")
        old_time = now
        while now - old_time < datetime.timedelta(seconds=5):
            now = datetime.datetime.now(pytz.utc)
            write_line(log_file)

        print("Back to low traffic")
        old_time = now
        while True:
            now = datetime.datetime.now(pytz.utc)
            time.sleep(0.02)
            write_line(log_file)
