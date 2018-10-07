from collections.__init__ import defaultdict
from functools import total_ordering


@total_ordering
class BasicStats:
    def __init__(self):
        self.timestamp = None
        self.trx_per_resource = defaultdict(int)
        self.trx_per_user = defaultdict(int)
        self.trx_per_method = defaultdict(int)
        self.trx_per_status = defaultdict(int)
        self.trx_per_sec = 0.0

    def __eq__(self, other):
        return self.timestamp == other.timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def reset(self, timestamp):
        self.timestamp = timestamp
        self.trx_per_resource = defaultdict(int)
        self.trx_per_user = defaultdict(int)
        self.trx_per_method = defaultdict(int)
        self.trx_per_status = defaultdict(int)
        self.trx_per_sec = 0.0
