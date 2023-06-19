#-*- coding:utf-8 -*-

"""Types
"""

__all__ = [
    "Any",
    "Boolean",
    "Integer",
    "Float",
    "String",
    "Bytes",
    "DefaultTuple",
    "DefaultList",
    "DefaultDict",
    "Object",
    "Namespace",
]

#
# Imports Modules
#
import typing as _typing

# Any Variables
Any = _typing.Any

# General Variables
Boolean = bool
Integer = int
Float = float
String = str
Bytes = bytes

# Default Variables
DefaultTuple = _typing.Tuple
DefaultList = _typing.List
DefaultDict = _typing.Dict

# Object Variables
class Object(object):
    """Object object
    """

    def __repr__(self) -> String:
        return "{CLASS}".format(CLASS=type(self).__name__)

# Namespace Variables
class Namespace(Object):
    """Namespace Object
    """

    def __repr__(self) -> String:
        return "Namespace:{CLASS}".format(CLASS=type(self).__name__)
