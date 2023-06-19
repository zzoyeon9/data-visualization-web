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
from controllers.create_Trend import *
from fastapi.templating import Jinja2Templates
#import Jinja2Templates

#Application
app = Application()

templates = Jinja2Templates

#WebAPIs
@app.object.get(
    '/vision/trend',
    response_class=HTMLResponse,
)




async def get_trend_on_html(request: Request, start_date: str, end_date: str, y_label: str)-> str:
    """
    Return Json Data of Trend Chart
    """

    ### 여기서 query로날짜를 특정해서 그 특정 날짜의 데이터만 DB에서 가져오게 수정해야함
    trend_df = create_DataFrame(start_date, end_date, y_label)
    trend_chart = create_Chart(trend_df, y_label)
    # item = visualize_Chart(trend_chart)
    item = output_Chart(trend_chart)
    
    max_value = max(trend_df[y_label])
    min_value = min(trend_df[y_label])
    avg_value = round(getAvgValue(trend_df, y_label), 2)
    median_value = getMedianValue(trend_df, y_label)

    item = addChartMetaData(item, y_label, max_value, min_value, avg_value, median_value)
    return item

"""
async def trend(request: Request):

    trends = trend_data()

	# Line차트
    line_chart = alt.Chart(trends).mark_line().transform_fold(
        ['MIXA_PASTEUR_TEMP', 'MIXB_PASTEUR_TEMP'],
        as_ = ['Temp', 'Value']
    ).encode(
        alt.Color('Temp:N'),
        alt.X('std_dt')
    )
	
    line1 = line_chart.transform_filter(
        alt.datum.Temp == 'MIXA_PASTEUR_TEMP'
    ).encode(
        alt.Y('a')
    ).interactive()
	
    line2 = line_chart.transform_filter(
        alt.datum.Temp == 'MIXB_PASTEUR_TEMP'
    ).encode(
        alt.Y('b')
    ).interactive()
	
    lines = alt.layer(line1, line2).resolve_scale(
        y = 'independent'
    )

	# Points
    point_chart = alt.Chart(trends).mark_point().transform_fold(
        ['MIXA_PASTEUR_TEMP', 'MIXB_PASTEUR_TEMP'],
        as_ = ['Temp', 'Value']
    ).encode(
        alt.Color('Temp:N'),
        alt.X('std_dt')
    )

    point1 = point_chart.transform_filter(
        alt.datum.Temp == 'MIXA_PASTEUR_TEMP'
    ).encode(
        alt.Y('a'),
        alt.Color('insp',
            alt.Scale(domain=['ng'], range=['red'])
        )
    ).interactive()

    point2 = point_chart.transform_filter(
    alt.datum.Temp == 'MIXB_PASTEUR_TEMP'
    ).encode(
        alt.Y('b')
    ).interactive()

    points = alt.layer(point1, point2).resolve_scale(
        y = 'independent'
    )

	# Line + Point
    charts = alt.layer(lines, points).resolve_scale(
        y = 'independent'
    ).properties(
        width=1000,
        height=800
    )

    chart_html = charts.to_html()

    return app.templates.TemplateResponse(
        "trend_chart.html", {
            "request": request, 
            "chart": chart_html
        }
    )

"""

