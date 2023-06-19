#-*- coding:utf-8 -*-

"""Configuration
"""

#
# Imports Modules
#
import os
import json
from modules import root
from modules.exceptions import *
from modules.types import *

#
# Objects
#
class Config(Object):
    """Config Object
    """

    # Instance Object
    _instance = None

    # Default Parameters
    _parameters = {
        "name": "Front-Project",
        "description": "",
        "version": "0.0.0",
        "dependencies": {},
        "path": {
            "root": os.path.join(root(), "views"),
            "views": os.path.join(root(), "views"),
            "static": os.path.join(root(), "static"),
        },
        "logger": {
            "log_level": "info",
            "log_path": "",
            "log_prefix": "front",
            "log_suffix": ".%Y%m%d.log",
            "log_when": "d",
            "log_interval": 1,
            "log_encoding": "utf-8",
            "log_fmt": "[{levelname}][{asctime}] - {message}",
            "log_style": "{",
            "log_use_colors": True,
        }
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # New Object
            cls._instance = new_object(cls, *args, **kwargs)
        return cls._instance

    @property
    def object(self) -> DefaultDict:
        return self._parameters

    @property
    def name(self) -> String:
        return String(self.get("name"))

    @property
    def description(self) -> String:
        return String(self.get("description"))

    @property
    def version(self) -> String:
        return String(self.get("version"))

    @property
    def dependencies(self) -> DefaultList:
        return self.get("dependencies")

    @property
    def logger(self) -> DefaultDict:
        return self.get("logger")

    @classmethod
    def reload(self):
        """Reload parameters of the config
        """

        load_config()

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

        return self.object.get(key, default)

#
# Functions
#
def new_object(cls, *args, **kwargs) -> Config:
    # Allocate instance
    instance = object.__new__(cls, *args, **kwargs)
    
    # Load Configure
    load_config(instance)
    
    return instance

def load_config(cls: Config):
    # Check 'config.json'
    configfile = os.path.join(root(), os.path.join("config", 'config.json'))
    if not os.path.exists(configfile):
        message = "FileNotFound: 'config.json'"
        raise ConfigNotFoundError(message)
    # Load 'config.json'
    src = ""
    with open(configfile) as fd:
        src = fd.read()
    if len(src) == 0:
        message = "NotLoadError: 'config.json'"
        raise ConfigNotLoadError(message)
    # Set parameters
    obj = json.loads(src)
    cls._parameters.update(obj)
