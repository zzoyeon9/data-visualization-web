#-*- coding:utf-8 -*-

"""Wrapper
"""

__all__ = [
    "FastAPIWrapper",
    "Jinja2TemplatesWrapper",
]

#
# Imports Modules
#

from fastapi import FastAPI as FastAPI
from fastapi.templating import Jinja2Templates as Jinja2Templates
from modules.config import Config
from modules.types import *

#
# Objects
#
class FastAPIWrapper(Object):
    """FastAPI Wrapper Object
    """

    # Instance Object
    _instance = None

    # FastAPI Object
    _fastapi: FastAPI=None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # New Object
            cls._instance = new_object_fastapi(cls, *args, **kwargs)            
        return cls._instance

    @property
    def object(self) -> FastAPI:
        return self._fastapi

class Jinja2TemplatesWrapper(Object):
    """Jinja2Templates Wrapper Object
    """

    # Instance Object
    _instance = None

    # Jinja2 Templates Object
    _templates: Jinja2Templates=None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # New Object
            cls._instance = new_object_templates(cls, *args, **kwargs)
        return cls._instance

    @property
    def object(self) -> Jinja2Templates:
        return self._templates

#
# Functions
#
def new_object_fastapi(cls, *args, **kwargs) -> FastAPIWrapper:
    """New Fastapi Object

    Returns
    -------
    :FastAPIWrapper :Wrapping FastAPI Instance

    """
    
    # Allocate instance
    instance: FastAPIWrapper=object.__new__(cls, *args, **kwargs)
    
    # Get config
    config = Config()

    # Set FastAPI's application
    instance._fastapi = FastAPI(
        title=config.name,
        description=config.description,
        version=config.version,
        debug=False,
    )
    
    return instance

def new_object_templates(cls, *args, **kwargs) -> Jinja2TemplatesWrapper:
    """New Fastapi Object

    Returns
    -------
    :Jinja2TemplatesWrapper :Wrapping Jinja2Templates Instance

    """

    # Allocate instance
    instance: Jinja2TemplatesWrapper=object.__new__(cls, *args, **kwargs)
    
    # Get Paths
    path: DefaultDict=Config().get('path')

    # Set templates
    instance._templates = Jinja2Templates(directory=path.get('views'))
    
    return instance
