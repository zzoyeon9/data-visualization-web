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

from controllers.create_Scatter_plot import *

import jinja2

#
# Application
#
app = Application()

#
# WebAPIs
#
@app.object.get(
    '/vision/scatter_plot',
    response_class=HTMLResponse
)
async def get_scatter_plot_on_html(request: Request, 
                                   start_date: str, end_date: str):
    """
    Return to scatter plot chart to json
    """

    scatter_Chart = makeScatterChart(
        createScatterDataFrame(start_date, end_date)
    )
    
    return outputChart(scatter_Chart)

