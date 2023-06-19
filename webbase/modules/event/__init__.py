#-*- coding:utf-8 -*-

"""Event
"""

__all__ = [
    "Event",
]

#
# Imports Moudules
#
from modules.application import Application
from modules.types import *

#
# Objects
#
class Event(Namespace):
    """Namespace: Event
    """

    @staticmethod
    def on_startup(app: Application):
        """Startup event

        Parameters
        ----------
        app: Application: Web Application

        """

        message = "Started front process."
        app.logger.info(message)

    @staticmethod
    def on_shutdown(app: Application):
        """Shutdown event

        Parameters
        ----------
        app: Application: Web Application

        """

        message = "Finished front process."
        app.logger.info(message)
