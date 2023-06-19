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

from controllers.create_Spc import *
import jinja2

#
# Application
#
app = Application()

#
# WebAPIs
#
@app.object.get(
    '/vision/spc',
    response_class=HTMLResponse ## Json형태로 반환하고 싶다면 JSONResponse로 변경
)
async def get_spc_on_html(request: Request, start_date: str, end_date: str, label: str) -> str:
    """
    create spc chart to json
    """

    data_list = get_Data_list(start_date, end_date, label)

    x_bar_y_series = get_X_bar_y_series(data_list)
    x_bar_x_series = get_X_bar_x_series(x_bar_y_series)
    

    u = round(sum(x_bar_y_series)/len(x_bar_y_series), 2)
    sigma = get_sigma(x_bar_y_series, u)

    lcl = u - 3*sigma
    ucl = u + 3*sigma

    X_bar_df = create_X_bar_dataFrame(x_bar_x_series, x_bar_y_series, u, sigma)
    X_bar_chart = create_X_bar_chart(X_bar_df, lcl, ucl)

    R_y_series = get_R_y_series(data_list)
    R_x_series = get_R_x_series(R_y_series)
   

    u = round(sum(R_y_series) / len(R_y_series), 2)
    sigma = get_sigma(R_y_series, u)

    R_df = create_R_dataFrame(R_x_series, R_y_series, u, sigma)
    R_chart = create_R_chart(R_df)

    return output_Chart(alt.vconcat(X_bar_chart, R_chart, spacing=-2))




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
