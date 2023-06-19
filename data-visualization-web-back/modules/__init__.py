#-*- coding:utf-8 -*-

#
# Imports Modules
#
import os
import sys
from pathlib import Path

#
# Append the path of the module to sys.path
#
__module__ = os.path.dirname(os.path.abspath(__file__))
if __module__ not in sys.path:
    sys.path.append(__module__)

def libpath() -> Path:
    """Returns fullpath of module.

    Returns
    -------
    :Path :Fullpath of module

    """

    return __module__

#
# Append the path of the main to sys.path
#
__root__ = os.path.dirname(__module__)
if __root__ not in sys.path:
    sys.path.append(__root__)

def root() -> Path:
    """Returns fullpath of root.

    Returns
    -------
    :Path :Fullpath of Root

    """

    return __root__
