#-*- coding:utf-8 -*-

__all__ = [
    "Service",
]

#
# Import modules
#
import os
import logging
import uvicorn
import uvicorn.config
from setproctitle import setproctitle
from modules.types import *
from modules.logger import *
from modules.logger.formatter import *
from modules.logger.handler import *

#
# Objects
#
class Service(Object):
    """Service
    """

    def run_forever(
            self, 
            host: String, 
            port: Integer,
            reload: Boolean,
        ):
        """Run forever on the service.

        Parameters
        ----------
        host: String: Hostname

        port: Integer: Port

        """

        try:
            self.__initialize__()
            self.__run__(
                host=host,
                port=port,
                reload=reload,
            )
        finally:
            self.__finalize__()

    def __initialize__(self, **kwargs):
        # Uvicorn Log Parameters
        logger = Logger()
        log_level: String=logger.get("log_level")
        log_path: String=logger.get("log_path")
        log_prefix: String=logger.get("log_prefix")
        log_suffix: String=logger.get("log_suffix")
        log_when: String=logger.get("log_when")
        log_interval: Integer=logger.get("log_interval")
        log_encoding: String=logger.get("log_encoding")
        log_fmt: String=logger.get("log_fmt")
        log_style: String=logger.get("log_style")
        log_use_colors: String=logger.get("log_use_colors")
        log_formatter = ColourizedFormatter

        # Uvicorn Log: Default
        self._set_uvicorn_log_for_default(
            log_level, log_path, log_prefix, log_suffix, log_when,
            log_interval, log_encoding, log_fmt, log_style, 
            log_use_colors, log_formatter,
        )

        # Uvicorn Log: Access
        self._set_uvicorn_log_for_access(
            log_level, log_path, log_prefix, log_suffix, log_when,
            log_interval, log_encoding, log_fmt, log_style, 
            log_use_colors, log_formatter,
        )

        # Uvicorn Log: Error
        self._set_uvicorn_log_for_error(
            log_level, log_path, log_prefix, log_suffix, log_when,
            log_interval, log_encoding, log_fmt, log_style, 
            log_use_colors, log_formatter,
        )

    def __finalize__(self, **kwargs):
        pass

    def __run__(cls, **kwargs):
        config = {}

        # App
        config["app"] = "app:__app__.object"

        # Host
        config["host"] = kwargs["host"]

        # Port
        config["port"] = kwargs["port"]

        # Reload
        config["reload"] = kwargs["reload"]

        # Log level
        if "log_level" in kwargs:
            config["log_level"]=kwargs["log_level"]
        else:
            logger = Logger()
            config["log_level"]=logger.get("log_level") 

        # Set Process Title
        proctitle = "Python Web Service"
        setproctitle(proctitle)

        # Run Service
        uvicorn.run(**config)

    def _set_uvicorn_log_for_default(
            self, 
            log_level: String,
            log_path: String,
            log_prefix: String,
            log_suffix: String,
            log_when: String,
            log_interval: Integer,
            log_encoding: String,
            log_fmt: String,
            log_style: String,
            log_use_colors: Boolean,
            log_formatter: logging.Formatter,
        ):
        """Setting uvicorn log for 'default'

        Parameters
        ----------
        log_level: String: log Level

        log_path: String: log path

        log_prefix: String: log prfix

        log_suffix: String: log suffix

        log_when: String: log when 
            
            Notes
            -----
            'S': Seconds,
            'M': Minutes,
            'H': Hours,
            'D': Days,
            'midnight': roll over at midnight,
            'W{0-6}': roll over on a certain day; 0 - Monday,

        log_interval: Integer: log interval

        log_encoding: String: log encoding

        log_fmt: String: log fmt info

        log_style: String: log style info

        log_use_colors: Boolean: log uses colors or not

        log_formatter: logging.Formatter: log formatter object

        """

        #
        # Uvicorn Log Formatters
        #
        uvicorn.config.LOGGING_CONFIG['formatters']['default'] = {}
        uvicorn.config.LOGGING_CONFIG['formatters']['default']['()'] = log_formatter
        uvicorn.config.LOGGING_CONFIG['formatters']['default']['fmt'] = log_fmt
        uvicorn.config.LOGGING_CONFIG['formatters']['default']['style'] = log_style
        uvicorn.config.LOGGING_CONFIG['formatters']['default']['use_colors'] = log_use_colors

        #
        # Uvicorn Log Handlers
        #
        uvicorn.config.LOGGING_CONFIG['handlers']['default'] = {}
        if Boolean(len(log_path)):
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['class'] = 'modules.logger.handler.TimedRotatingFileHandler'
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['when'] = log_when
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['interval'] = log_interval
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['encoding'] = log_encoding
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['formatter'] = 'default'
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['filename'] = os.path.join(log_path, log_prefix+'-default')
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['suffix'] = log_suffix
        else:
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['class'] = 'modules.logger.handler.StreamHandler'
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['formatter'] = 'default'
            uvicorn.config.LOGGING_CONFIG['handlers']['default']['stream'] = 'ext://sys.stdout'

        #
        # Uvicorn Log Loggers
        #
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn'] = {}
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn']['handlers'] = ['default']
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn']['level'] = log_level.upper()
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn']['propagate'] = False

    def _set_uvicorn_log_for_access(
            self, 
            log_level: String,
            log_path: String,
            log_prefix: String,
            log_suffix: String,
            log_when: String,
            log_interval: Integer,
            log_encoding: String,
            log_fmt: String,
            log_style: String,
            log_use_colors: String,
            log_formatter: logging.Formatter,
        ):
        """Setting uvicorn log for 'access'

        Parameters
        ----------
        log_level: String: log Level

        log_path: String: log path

        log_prefix: String: log prfix

        log_suffix: String: log suffix

        log_when: String: log when 
            
            Notes
            -----
            'S': Seconds,
            'M': Minutes,
            'H': Hours,
            'D': Days,
            'midnight': roll over at midnight,
            'W{0-6}': roll over on a certain day; 0 - Monday,

        log_interval: Integer: log interval

        log_encoding: String: log encoding

        log_fmt: String: log fmt info

        log_style: String: log style info

        log_use_colors: Boolean: log uses colors or not

        log_formatter: logging.Formatter: log formatter object

        """

        #
        # Uvicorn Log Formatters
        #
        uvicorn.config.LOGGING_CONFIG['formatters']['access'] = {}
        uvicorn.config.LOGGING_CONFIG['formatters']['access']['()'] = log_formatter
        uvicorn.config.LOGGING_CONFIG['formatters']['access']['fmt'] = log_fmt
        uvicorn.config.LOGGING_CONFIG['formatters']['access']['style'] = log_style
        uvicorn.config.LOGGING_CONFIG['formatters']['access']['use_colors'] = log_use_colors

        #
        # Uvicorn Log Handlers
        #
        uvicorn.config.LOGGING_CONFIG['handlers']['access'] = {}
        if Boolean(len(log_path)):
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['class'] = 'modules.logger.handler.TimedRotatingFileHandler'
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['when'] = log_when
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['interval'] = log_interval
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['encoding'] = log_encoding
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['formatter'] = 'access'
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['filename'] = os.path.join(log_path, log_prefix+'-access')
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['suffix'] = log_suffix
        else:
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['class'] = 'modules.logger.handler.StreamHandler'
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['formatter'] = 'access'
            uvicorn.config.LOGGING_CONFIG['handlers']['access']['stream'] = 'ext://sys.stdout'

        #
        # Uvicorn Log Loggers
        #
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn.access'] = {}
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn.access']['handlers'] = ['access']
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn.access']['level'] = log_level.upper()
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn.access']['propagate'] = False

    def _set_uvicorn_log_for_error(
            self, 
            log_level: String,
            log_path: String,
            log_prefix: String,
            log_suffix: String,
            log_when: String,
            log_interval: Integer,
            log_encoding: String,
            log_fmt: String,
            log_style: String,
            log_use_colors: Boolean,
            log_formatter: logging.Formatter,
        ):
        """Setting uvicorn log for 'error'

        Parameters
        ----------
        log_level: String: log Level

        log_path: String: log path

        log_prefix: String: log prfix

        log_suffix: String: log suffix

        log_when: String: log when 
            
            Notes
            -----
            'S': Seconds,
            'M': Minutes,
            'H': Hours,
            'D': Days,
            'midnight': roll over at midnight,
            'W{0-6}': roll over on a certain day; 0 - Monday,

        log_interval: Integer: log interval

        log_encoding: String: log encoding

        log_fmt: String: log fmt info

        log_style: String: log style info

        log_use_colors: Boolean: log uses colors or not

        log_formatter: logging.Formatter: log formatter object

        """

        #
        # Uvicorn Log Formatters
        #
        uvicorn.config.LOGGING_CONFIG['formatters']['error'] = {}
        uvicorn.config.LOGGING_CONFIG['formatters']['error']['()'] = log_formatter
        uvicorn.config.LOGGING_CONFIG['formatters']['error']['fmt'] = log_fmt
        uvicorn.config.LOGGING_CONFIG['formatters']['error']['style'] = log_style
        uvicorn.config.LOGGING_CONFIG['formatters']['error']['use_colors'] = log_use_colors

        #
        # Uvicorn Log Handlers
        #
        uvicorn.config.LOGGING_CONFIG['handlers']['error'] = {}
        if Boolean(len(log_path)):
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['class'] = 'modules.logger.handler.TimedRotatingFileHandler'
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['when'] = log_when
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['interval'] = log_interval
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['encoding'] = log_encoding
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['formatter'] = 'error'
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['filename'] = os.path.join(
                log_path, 
                log_prefix+'-error',
            )
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['suffix'] = log_suffix
        else:
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['class'] = 'modules.logger.handler.StreamHandler'
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['formatter'] = 'error'
            uvicorn.config.LOGGING_CONFIG['handlers']['error']['stream'] = 'ext://sys.stdout'

        #
        # Uvicorn Log Loggers
        #
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn.error'] = {}
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn.error']['handlers'] = ['error']
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn.error']['level'] = log_level.upper()
        uvicorn.config.LOGGING_CONFIG['loggers']['uvicorn.error']['propagate'] = False
