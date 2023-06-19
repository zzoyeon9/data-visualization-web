
#-*- coding:utf-8 -*-

from models.get_Trend_data import *
import altair as alt
import pandas as pd
import numpy as np
import json

def getAvgValue(df: pd.DataFrame, y_label: str)-> str:
    """
    Return y_label's average value
    """

    return np.mean(df[y_label])



def getMedianValue(df: pd.DataFrame, y_label: str)-> str:
    """
    Return y_label's median Value
    """

    return np.median(df[y_label].dropna())



def create_DataFrame(start_date: str, end_date : str, y_label: str)-> pd.DataFrame:
    """
    Create dataframe of Trend chart
    and return it.
    """

    date_x = get_Date_Series(start_date, end_date)
    y_series = get_Y_Series(start_date, end_date, y_label)
    df = pd.DataFrame({"Date": date_x.to_list(), 
                       y_label: y_series.to_list()})
    return df



def create_Chart(df : pd.DataFrame, y_label: str)-> alt.Chart():
    """
    Create Trend chart
    and return it.
    """

    trend_chart = alt.Chart(df).mark_line(color='blue').encode(
        x=alt.X('Date', axis = alt.Axis(title='날짜')), 
        y=alt.Y(y_label, scale = alt.Scale(domain=[df[y_label].min() - 10, 
                                               df[y_label].max() + 10]), 
                axis = alt.Axis(title='A살균기의  살균 온도')), 
        tooltip=[y_label],
    ).properties(width=700, height=350).interactive()

    """
    B_chart = alt.Chart(df).mark_line(color='red').encode(
        x=alt.X('Date', axis = alt.Axis(title='Timestamp')), 
        y=alt.Y('B', axis = alt.Axis(title='mixb_pasteur_temp')),
        tooltip=['B']
    ).properties(width=700, height=400).interactive()
    """
    return trend_chart



def addChartMetaData(chart_data: str, y_label: str, max_value: str, 
                     min_value: str, avg_value: str, median_value: str)-> str:
    """
    Return Trend chart's Metadata.
    """
    json_data = json.loads(chart_data)
    json_data['max'] = max_value
    json_data['min'] = min_value
    json_data['avg'] = avg_value
    json_data['median'] = median_value
    
    final_data = json.dumps(json_data)

    return final_data


def visualize_Chart(chart : alt.vegalite.v4.api.Chart): 
    """
    Visualizing the Trend Chart.
    """

    return chart.to_html()

def output_Chart (chart : alt.vegalite.v4.api.Chart): 
    """
    Return Trend chart's Json data from chart.
    """

    return chart.to_json()

