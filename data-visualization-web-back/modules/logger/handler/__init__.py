#-*- coding:utf-8 -*-

"""Logger Handlers
"""

__all__ = [
    "StreamHandler",
    "TimedRotatingFileHandler",
]

#
# Imports Modules
#
import logging
import logging.handlers
from modules.types import *

#
# Objects
#

class StreamHandler(logging.StreamHandler):
    """StreamHandler
    """

    pass

class TimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """TimedRotatingFileHandler
    """

    def __init__(self, filename, when='h', interval=1, backupCount=0, 
                encoding=None, delay=False, utc=False, atTime=None, 
                suffix=''):
        super(TimedRotatingFileHandler, self).__init__(
            filename=filename,
            when=when,
            interval=interval,
            backupCount=backupCount,
            encoding=encoding, 
            delay=delay,
            utc=utc,
            atTime=atTime,
        )
        if Boolean(len(suffix)):
            self.suffix = suffix
