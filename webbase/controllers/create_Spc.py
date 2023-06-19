#-*- coding:utf-8 -*-

from models.get_Spc_data import *
import altair as alt
import pandas as pd
import numpy as np
import math

def get_Data_list(start_date: str, end_date: str, label: str) -> list:
    """
    return label's list
    """
    return get_MIXA_TEMP(start_date, end_date, label)



def get_sigma(series : list, u : float): 
    """
    표준 편차 반환
    """

    temp = 0

    for i in series:
        temp += (u - i) ** 2

    temp = round((temp/len(series))**0.5, 2)

    return temp



def get_X_bar_y_series(data_list: str):
    """
    Return X_bar y series's list
    """

    y_series = []

    temp = 0
    count = 0

    for i in data_list:
        temp += i
        count += 1

        if count >= 5:
            y_series.append(round(temp/5.0, 2))
            count = 0
            temp = 0

    return y_series



def get_X_bar_x_series(y_series: list): 
    """
    Return X_bar x series's list
    """

    x_series = [round(i, 2) for i in range(0, len(y_series))]

    return x_series



def get_R_x_series(y_series: list):
    """
    Return R chart's x series list
    """

    x_series = [round(i, 2) for i in range(0, len(y_series))]

    return x_series



def get_R_y_series(data_list: list):
    """
    Return R chart's y series list
    """

    y_series = []

    tempList = []
    count = 0

    for i in data_list:
        tempList.append(i)
        count += 1

        if count >= 5:
            y_series.append(round(max(tempList) - min(tempList), 2))
            count = 0
            tempList = []

    return y_series



def create_R_dataFrame(x_series : list, y_series : list, u : float, sigma : float):
    """
    R df 반환
    """

    R_dataFrame = pd.DataFrame({"R_x": x_series, 
                                 "R_y": y_series})
    
    R_dataFrame['UCL'] = u + (3 * sigma)
    R_dataFrame['LCL'] = u - (3 * sigma)
    R_dataFrame['u'] = u

    return R_dataFrame



def create_X_bar_dataFrame(x_series : list, y_series : list, u : float, sigma : float):
    """
    X_bar df 반환
    """

    X_bar_dataFrame = pd.DataFrame({"X_bar_x": x_series, 
                                     "X_bar_y": y_series})
    
    X_bar_dataFrame['UCL'] = u + (3 * sigma)
    X_bar_dataFrame['LCL'] = u - (3 * sigma)
    X_bar_dataFrame['u'] = u

    return X_bar_dataFrame



def create_X_bar_chart(X_bar_df : pd.DataFrame, lcl: float, ucl: float):
    """
    X_bar 차트 반환
    """

    X_bar_chart = alt.Chart(X_bar_df)

    X_bar = X_bar_chart.mark_line().encode(
        x=alt.X('X_bar_x:Q', axis = alt.Axis(title='표본')),
        y=alt.Y('X_bar_y:Q', axis=alt.Axis(title='표본  평균'), 
                scale=alt.Scale(domain=[lcl - 10, ucl + 10])),
        tooltip=['X_bar_y'],
    ).properties(width=500, height=110).interactive()

    ucl_chart = X_bar_chart.mark_rule(color='red').encode(y='UCL',
                                                          tooltip=['UCL'])
    lcl_chart = X_bar_chart.mark_rule(color='red').encode(y='LCL',
                                                          tooltip=['LCL'])
    ucl_chart.configure_axis(labels=False)
    lcl_chart.configure_axis(labels=False)
    u = X_bar_chart.mark_rule().encode(y=alt.Y('u'), color=alt.value('green'),
                                       tooltip=['u'])

    ucl_text = X_bar_chart.mark_text(align='center', dx=390, dy=-5).encode(
        y = alt.Y('UCL'), text = alt.value('UCL'))#.configure_mark(fontSize=10)
    lcl_text = X_bar_chart.mark_text(align='center', dx=390, dy=-5).encode(
        y = alt.Y('LCL'), text = alt.value('LCL'))
    u_text = X_bar_chart.mark_text(align='center', dx=390, dy=-5).encode(
        y = alt.Y('u'), text = alt.value('u'))
    
    chart = X_bar + ucl_chart + lcl_chart + u + ucl_text + lcl_text + u_text
    return chart#.interactive()



def create_R_chart(R_df : pd.DataFrame):
    """
    R 차트 반환
    """

    R_chart = alt.Chart(R_df)

    R = R_chart.mark_line().encode(
        x=alt.X('R_x:Q', axis=alt.Axis(title='표본')),
        y=alt.Y('R_y:Q', scale = alt.Scale(domain=[R_df['R_y'].min()-3, 
                                                   R_df['R_y'].max()+3]), 
                axis=alt.Axis(title='표본 범위')), 
        tooltip=['R_y']).properties(width=500, height=110)

    ucl = R_chart.mark_line().encode(x='R_x', y='UCL', color=alt.value('red'),
                                     tooltip=['UCL'])
    lcl = R_chart.mark_line().encode(x='R_x', y='LCL', color=alt.value('red'),
                                     tooltip=['LCL'])
    ucl.configure_axis(labels=False)
    lcl.configure_axis(labels=False)
    u = R_chart.mark_line().encode(x='R_x', y='u', color=alt.value('green'),
                                   tooltip=['u'])

    ucl_text = R_chart.mark_text(align='center', dx=390, dy=1).encode(
        y = alt.Y('UCL'), text = alt.value('UCL'))
    lcl_text = R_chart.mark_text(align='center', dx=390, dy=1).encode(
        y = alt.Y('LCL'), text = alt.value('LCL'))
    u_text = R_chart.mark_text(align='center', dx=390, dy=1).encode(
        y = alt.Y('u'), text = alt.value('u'))
    
    chart = R + ucl + lcl + u + ucl_text + lcl_text + u_text
    
    return chart.interactive()



def output_Chart(chart : alt.vegalite.v4.api.Chart): 
    """
    chart to html
    """

    return chart.to_json()

