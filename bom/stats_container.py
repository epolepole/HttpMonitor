from bom.average_stats import AverageStats


class StatsContainer:
    def __init__(self):
        self.average_stats_dict = {}

    def add_avg_stats(self, time_period):
        self.average_stats_dict[time_period] = AverageStats(time_period)

    def get_avg_stats(self, time_period):
        return self.average_stats_dict.get(time_period)
