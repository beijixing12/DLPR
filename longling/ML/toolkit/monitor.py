"""Compact monitor utilities used by EduSim training loops.

These are lightweight stand-ins for the upstream ``longling.ML.toolkit.monitor``
components and intentionally implement only the methods exercised in this
project.
"""

from typing import Iterable, Iterator

__all__ = ["ConsoleProgressMonitor", "EMAValue"]


class ConsoleProgressMonitor:
    def __init__(self, indexes=None, values=None, total=None, player_type=None):
        self.total = total

    def __call__(self, iterable: Iterable) -> Iterator:
        return iter(iterable)


class EMAValue(dict):
    def __init__(self, keys):
        super().__init__()
        for k in keys:
            self[k] = 0.0
