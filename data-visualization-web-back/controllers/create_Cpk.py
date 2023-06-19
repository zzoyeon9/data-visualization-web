#-*- coding:utf-8 -*-

from models.get_Cpk_data import *
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math, json
from scipy.stats import norm


def get_Data_list(start_date: str, end_date: str, label: str):
    """
    return specific label's value list
    """
    
    return get_MIXA_TEMP(start_date, end_date, label)




def get_length():
    """
    시리즈 개수 반환
    """

    kinds = set()
    
    for i in data_list:
        kinds.add(i)

    return len(kinds)




def get_Cpk_x_series(data_list: list):
    """
    cpk 내 x 시리즈 반환
    """

    x_series = []
    max_value = max(data_list)

    x_series = [round(i, 1) for i in np.arange(0, max_value, 0.1)]
    return x_series



def get_Cpk_y_series(x_series: list, data_list: list): 
    """
    cpk 내 y 시리즈 반환
    """
    
    y_series = [0 for i in range(len(x_series))]
    idx = 0

    for i in np.arange(0, max(x_series), 0.1):

        y_series[idx] = data_list.count(round(i, 1))
        idx += 1
    return y_series



def get_sigma(u : int, data_list):
    """
    표준편차 반환
    """

    sum = 0

    for i in data_list:
        sum += (u - i) ** 2

    sum /= len(data_list)
    result = sum ** 0.5

    return result



def get_avg(data_list: list): 
    """
    평균 반환
    """

    return sum(data_list) / len(data_list)



def getMedian(data_list: list):
    """
    메디안(중앙값) 반환
    """

    arr = sorted(data_list)
    a_len = len(arr) 


    # 빈 배열은 에러 반환
    if (a_len == 0): 
        return None

     # 요소 개수의 절반값 구하기
    a_center = int(a_len / 2)

    # 요소 개수가 홀수면
    # 홀수 개수인 배열에서는 중간 요소를 그대로 반환
    if (a_len % 2 == 1):
        return arr[a_center]
    else:
        # 짝수 개 요소는, 중간 두 수의 평균 반환
        return (arr[a_center - 1] + arr[a_center]) / 2.0 


def get_Nd_x_series(data_list: list):
    """
    정규분포 그래프 x 시리즈 반환
    """

    max_value = max(data_list)
    min_value =  min(data_list)
    nd_x_series = []

    for i in np.arange((min_value - 15), (max_value + 15), 0.05):
        nd_x_series.append(round(i,1))

    return nd_x_series



def get_Nd_y_series(u : float, sigma : float, nd_x_series : list):
    """
    확률밀도함수를 이용하여 그래프 y 시리즈 반환
    """

    nd_y_series = norm.pdf(nd_x_series, loc = u, scale=sigma)
    nd_y_series = np.round(nd_y_series, 4)
    
    return nd_y_series



def create_Nd_DataFrame(line_x_series : list, line_y_series : list):
    """
    cpk 데이터프레임 생성
    """

    nd_df = pd.DataFrame({'Percentage variable': line_x_series, 
                          'Percentage': line_y_series}) 
    return nd_df



def create_Block_DataFrame(bar_x_series : list, bar_y_series : list, usl : float, lsl : float, u : float):
    """
    cpk 데이터프레임 생성
    """

    bar_df = pd.DataFrame({'Measurement': bar_x_series, 
                           'Frequency': bar_y_series, 
                           'USL': usl, 'LSL': lsl, 'u': u})
    
    return bar_df



def create_Cpk_chart(bar_df : pd.DataFrame, nd_df : pd.DataFrame):
    """
    cpk 차트 생성
    """

    bar = alt.Chart(bar_df).mark_bar(color='blue', size=20).encode(
        x=alt.X('Measurement:Q', axis=alt.Axis(title='측정값')),
        y=alt.Y('Frequency:Q', 
                axis=alt.Axis(title='빈도수')),
        
        tooltip=['Frequency'],
        #color = alt.Color('Origin', range=col)
    ).properties(width=500, height=150).interactive()

    line = alt.Chart(nd_df).mark_line(color='black').encode(
        x=alt.X('Percentage variable', scale = alt.Scale(
            domain=[nd_df['Percentage variable'].min(), 
                    nd_df['Percentage variable'].max()]),
            axis = alt.Axis(title='')), 
        y=alt.Y('Percentage', 
                axis = alt.Axis(title='확률')),
        tooltip=['Percentage']
    ).properties(width=500, height=150).interactive()

    rule_USL = alt.Chart(bar_df).mark_rule(color='red').encode(
        x='USL', tooltip=['USL'])
    rule_LSL = alt.Chart(bar_df).mark_rule(color='red').encode(
        x='LSL', tooltip=['LSL'])
    rule_USL.configure_axis(labels=False)
    rule_LSL.configure_axis(labels=False)

    rule_M = alt.Chart(nd_df).mark_rule(color='green').encode(x='m:Q')

    text_USL = alt.Chart(bar_df).mark_text(align='left', dx=3, dy=-230).encode(
        alt.X('USL:Q'), text=alt.value('USL'))
    text_LSL = alt.Chart(bar_df).mark_text(align='left', dx=3, dy=-230).encode(
        alt.X('LSL:Q'), text=alt.value('LSL'))
    text_M = alt.Chart(bar_df).mark_text(align='left', dx=3, dy=-230).encode(
        alt.X('m:Q'), text=alt.value('m'))

    bar_chart = bar + rule_USL + rule_LSL + rule_M + text_USL + text_LSL + text_M
    line_chart = line

    cpk_chart = alt.layer(bar_chart, line_chart).resolve_scale(x='shared', y='independent')

    return cpk_chart
 


def addChartMetaData(chart_data: str, sigma: str, cp: str, cpk: str)-> str:
    """
    Return Trend chart's Metadata.
    """

    json_data = json.loads(chart_data)
    json_data['sigma'] = sigma
    json_data['cp'] = round(cp, 2)
    json_data['cpk'] = round(cpk, 2)
    
    final_data = json.dumps(json_data)
    
    return final_data



def output_Chart(chart : alt.vegalite.v4.api.Chart): 
    """
    chart to html
    """
    return chart.to_json()

