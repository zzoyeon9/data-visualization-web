#-*- coding:utf-8 -*-

"""Event Router
"""

#
# Imports Moudules
#
from modules.application import Application
from modules.event import Event
from modules.types import *

#
# Application
#
app = Application()

#
# WebAPIs
#
@app.object.on_event("startup")
async def on_startup_event():
    """Startup event
    """

    Event.on_startup(app)

@app.object.on_event("shutdown")
async def on_shutdown_event():
    """Shutdown event
    """

    Event.on_shutdown(app)
