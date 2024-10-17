from .utils import trunc


def pretty_print(self, no_trunc=False):
    output = f"{self.start_time_str}-{self.end_time_str} | {trunc(self.project, None if no_trunc else 30)} | {trunc(self.comment, 30)}"
    return output
