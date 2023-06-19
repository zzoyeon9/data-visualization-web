from routes.trend_chart import *
from routes.scatter_plot import *
from routes.cpk_chart import *
from routes.spc_chart import *
from controllers.compression import *
from fastapi import APIRouter
from fastapi.responses import FileResponse

@app.object.get(
    '/download',
    response_class=HTMLResponse ## Json형태로 반환하고 싶다면 JSONResponse로 변경
)
async def downloadAllChartToJson(request: Request, start_date: str, end_date: str, label: str)-> str:
    """
    transfer zipfile to client
    """

    scatter_chart = await get_scatter_plot_on_html(request, start_date, end_date)
    trend_chart = await get_trend_on_html(request, start_date, end_date, label)
    cpk_chart = await get_Cpk_on_html(request, start_date, end_date, label)
    spc_chart = await get_spc_on_html(request, start_date, end_date, label)

    zip_file = await createZipFile(scatter_chart, trend_chart, cpk_chart, spc_chart)

    return FileResponse(zip_file, media_type='application/octet-stream',
                        filename='chart_data.zip')

