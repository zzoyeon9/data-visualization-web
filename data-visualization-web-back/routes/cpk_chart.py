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

from controllers.create_Cpk import *

import jinja2

#
# Application
#
app = Application()

#
# WebAPIs
#
@app.object.get(
    '/vision/cpk',
    response_class=HTMLResponse ## Json형태로 반환하고 싶다면 JSONResponse로 변경
)
async def get_Cpk_on_html(request: Request, start_date: str, end_date: str, label: str)-> str:
    """
    return cpk chart to json
    """

    data_list = get_Data_list(start_date, end_date, label)
    block_x_series = get_Cpk_x_series(data_list)
    block_y_series = get_Cpk_y_series(block_x_series, data_list)

    u = round(get_avg(data_list), 2)
    sigma = round(get_sigma(u, data_list), 2)
    usl = 70
    lsl = 50

    line_x_series = get_Nd_x_series(data_list)
    line_y_series = get_Nd_y_series(u, sigma, line_x_series)
    
    
    cpk_df = create_Block_DataFrame(block_x_series, block_y_series, usl, lsl, u)
    nd_df = create_Nd_DataFrame(line_x_series, line_y_series)
    cp = (usl - lsl) / 6 * sigma
    cpk = min((usl - u) / (3 * sigma), (u - lsl) / (3 * sigma))

    cpk_chart = create_Cpk_chart(cpk_df, nd_df)
    cpk_chart = output_Chart(cpk_chart)
    cpk_chart = addChartMetaData(cpk_chart, sigma, cp, cpk)
    
    return cpk_chart



"""
    return app.templates.TemplateResponse(
        "scatter_plot.html",
        { 
            "request" : request,
            #"data" : chart
        }
    )
"""
"""
@app.object.get('/scatter_plot_json',
                response_class=JSONResponse
)
async def get_scatter_plot_on_json():
    return "OK"
"""
