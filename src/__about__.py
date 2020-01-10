#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__"
]

MAJOR = 0
"""(int) Version major component."""
MINOR = 0
"""(int) Version minor component."""
POST = 1
"""(int) Version post or bugfix component."""

__title__ = "PiAlarmClock"
__summary__ = """
Raspberry Pi Python with Kivy for UI based alarm clock.
"""
__uri__ = "https://github.com/jlegrand62/PiAlarmClock"
__version__ = ".".join([str(s) for s in (MAJOR, MINOR, POST)])

__author__ = "Jonathan Legrand"
__email__ = "jlegrand62@gmail.com"
