#-*- coding:utf-8 -*-

"""AppMain
"""

# Require logger
from modules.logger import Logger
__logger__ = Logger()

# Require application
from modules.application import Application
__app__ = Application()
__logger__.object.info("Loaded application")

# Require routes
from routes import *
__logger__.object.info("Seted routers")
