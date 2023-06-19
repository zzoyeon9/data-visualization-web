#-*- coding:utf-8 -*-

"""Application
"""

__all__ = [
    'Application',
]

#
# Imports Modules
#
import logging
from fastapi import FastAPI as FastAPI
from fastapi.staticfiles import StaticFiles as StaticFiles
from fastapi.templating import Jinja2Templates as Jinja2Templates
from modules.config import Config
from modules.logger import Logger
from modules.wrapper import (
    FastAPIWrapper,
    Jinja2TemplatesWrapper,
)
from modules.types import *

#
# Objects
#
class Application(Object):
    """Application Object
    """

    # Instance Object
    _instance = None
    
    # FastAPI Application Object
    _application: FastAPIWrapper=None

    # Jinja2Template Object
    _templates: Jinja2TemplatesWrapper=None

    # Logger Object
    _logger: Logger=None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # New Object
            cls._instance = new_object(cls, *args, **kwargs)            
        return cls._instance

    @property
    def object(self) -> FastAPI:
        return self._application.object

    @property
    def templates(self) -> Jinja2Templates:
        return self._templates.object

    @property
    def logger(self) -> logging.Logger:
        return self._logger.object

#
# Functions
#
def new_object(cls, *args, **kwargs) -> Application:
    # Allocate instance
    instance: Application=object.__new__(cls, *args, **kwargs)
            
    # Set FastAPI Application
    instance._application = FastAPIWrapper()

    # Set Jinja2 Templates
    instance._templates = Jinja2TemplatesWrapper()

    # Set logger
    instance._logger = Logger()

    # Set static
    path: DefaultDict=Config().get('path')
    instance._application.object.mount(
        "/static", 
        StaticFiles(directory=path.get('static')), 
        name="static",
    )

    return instance
