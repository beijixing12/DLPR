"""Lightweight compatibility shims for the external ``longling`` package.

This stub implements only the small subset of helpers used by the project to
reduce external runtime dependencies. It is **not** a drop-in replacement for
upstream longling.
"""

import json
import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable

__all__ = [
    "as_io",
    "as_list",
    "wf_open",
    "config_logging",
    "path_append",
    "json_load",
    "abs_current_dir",
    "set_logging_info",
]


@contextmanager
def as_io(obj):
    """Accept a path-like or file-like object and yield a readable stream."""

    if hasattr(obj, "read"):
        yield obj
    else:
        with open(obj, "r", encoding="utf-8") as f:
            yield f


def as_list(obj):
    if obj is None:
        return []
    if isinstance(obj, (str, bytes)):
        return [obj]
    if isinstance(obj, Iterable):
        return list(obj)
    return [obj]


def wf_open(path, *args, **kwargs):
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not args:
        args = ("w",)
    return open(path, *args, encoding=kwargs.pop("encoding", "utf-8"), **kwargs)


def config_logging(level=logging.INFO, **kwargs):
    logging.basicConfig(level=level, **kwargs)


def set_logging_info(level=logging.INFO, **kwargs):
    config_logging(level=level, **kwargs)


def path_append(base, *paths):
    return str(Path(base).joinpath(*paths))


def json_load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def abs_current_dir(file_path):
    return str(Path(file_path).resolve().parent)


# Re-export subpackages expected by callers.
from .utils import stream  # noqa: E402,F401
