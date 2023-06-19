#-*- coding:utf-8 -*-

# API 호출

"""
Index Router
"""


#Import Modules
from fastapi import FastAPI
from modules.application import Application
from modules.request import Request
from modules.response import HTMLResponse
from models.get_Trend_data import trend_data
from controllers.create_Trend import *
from fastapi.templating import Jinja2Templates
#import Jinja2Templates

#Application
app = Application()

templates = Jinja2Templates

#WebAPIs
@app.object.get(
    '/trend',
    response_class=HTMLResponse,
)

async def trend(request: Request):
    trends = trend_data()

    line1 = alt.Chart(trends).mark_line(color='red').encode(
        x = 'std_dt',
        y = 'a'
#        color = alt.Color('insp')
    )

    line2 = alt.Chart(trends).mark_line(color='blue').encode(
        x = 'std_dt',
        y = 'b'
#        color = alt.Color('insp')
    )

    chart = alt.layer(line1, line2).resolve_scale(
#        x = alt.X('std_dt'),
        color = 'independent',
#        color = alt.value('origin')
#        color = 'origin:N'
#        color = alt.Color('insp')
    ).properties(
        width=1000,
        height=500
    ).interactive()    

    chart_html = chart.to_html()

    return app.templates.TemplateResponse(
        "trend_chart.html", {
            "request": request, 
            "chart": chart_html
        }
    )

