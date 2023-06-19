import zipfile
import json

async def createZipFile(trend_chart: str, scatter_plot_chart: str, 
                  cpk_chart: str, spc_chart: str):
    """
    return zipFile that contains all of chart's json data
    """
    
    with zipfile.ZipFile('chart_data.zip', 'w') as zipf:
        zipf.writestr('trend.json', trend_chart)
        zipf.writestr('scatter_plot.json', scatter_plot_chart)
        zipf.writestr('cpk.json', cpk_chart)
        zipf.writestr('spc.json', spc_chart)

    return 'chart_data.zip'
