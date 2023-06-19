#-*- coding:utf-8 -*-

__all__ = [
    "Logger",
]

#
# Imports Modules
#
import os
import logging
from modules.config import Config
from modules.types import *
from modules.logger.formatter import *
from modules.logger.handler import *

#
# Objects
#
class Logger(Object):
    """Logger Object
    """

    # Instance Object
    _instance = None

    # Logger
    _logger = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # New Object
            cls._instance = new_object(cls, *args, **kwargs)            
        return cls._instance

    @property
    def object(self) -> logging.Logger:
        return self._logger

    def get(self, key: String, default: Any=None) -> Any:
        """Config Getter

        Parameters
        ----------
        key: str: the key of parameters

        default: Any: default value, 'None'

        Returns
        -------
        :Any : the value for the key of parameters

        """

        return Config().logger.get(key, default)

#
# Functions
#
def new_object(cls, *args, **kwargs) -> Logger:
    
    # Allocate instance
    instance: Logger=object.__new__(cls, *args, **kwargs)

    # Load config
    config = Config()
    log_object = config.logger
    log_level = log_object.get("log_level")
    log_path = log_object.get("log_path")
    log_prefix = log_object.get("log_prefix")
    log_suffix = log_object.get("log_suffix")
    log_when = log_object.get("log_when")
    log_interval = log_object.get("log_interval")
    log_encoding = log_object.get("log_encoding")
    log_fmt = instance.get("log_fmt")
    log_style = instance.get("log_style")
    log_use_colors = instance.get("log_use_colors")
    log_formatter = ColourizedFormatter(
        fmt=log_fmt,
        style=log_style,
        use_colors=log_use_colors,
    )

    # Allocate the logger
    if instance._logger is None:

        # Create the logger
        logger = logging.getLogger()
        logger.setLevel({
            'debug': logging.DEBUG, 
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }.get(log_level, 'info'))

        # LogFile
        if Boolean(len(log_path)):
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            full_logpath = os.path.join(log_path, log_prefix)
            file_handler = TimedRotatingFileHandler(
                filename=full_logpath,
                when=log_when,
                interval=log_interval,
                encoding=log_encoding,
            )
            file_handler.suffix = log_suffix
            file_handler.setFormatter(log_formatter)
            logger.addHandler(file_handler)
        # Stream
        else:
            stream_handler = StreamHandler()
            stream_handler.setFormatter(log_formatter)
            logger.addHandler(stream_handler)

        # Set logger
        instance._logger = logger

    return instance
