#-*- coding:utf-8 -*-

"""Exceptions
"""

# Configuration
class ConfigNotFoundError(Exception): pass
class ConfigNotLoadError(Exception): pass

# Package
class PackageNotFoundError(Exception): pass

# Metadata
class MetadataAccessError(Exception): pass
