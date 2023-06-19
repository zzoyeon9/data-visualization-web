#-*- coding:utf-8 -*-

# API 호출 

"""Index Router
"""

#
# Imports Moudules
#
from modules.application import Application
from modules.request import Request
from modules.response import HTMLResponse

#
# Application
#
app = Application()

#
# WebAPIs
#
@app.object.get(
    '/',
    response_class=HTMLResponse,
)
async def on_get_root(request: Request):
    return app.templates.TemplateResponse(
        "index.html", {
            "request": request,
        }
    )
"""
import base64

@app.object.get(
    '/message',
)
async def on_get_message():
    return {
        "message" : "Send to Message",
        "status" : 200,
        "password" : base64.b64encode("Hansol123".encode()).decode()
    }
"""
