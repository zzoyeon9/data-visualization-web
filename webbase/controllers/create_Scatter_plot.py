#-*- coding:utf-8 -*-

from models.get_Scatter_data import *
import altair as alt
import pandas as pd



def createScatterDataFrame(start_date: str, end_date: str):  
    """
    Create Scatter plot chart's DataFrame
    """

    scatter_df = getScatterDataFrame(start_date, end_date)

    return scatter_df


def makeScatterChart(dataFrame):
    """
    Create Scatter plot chart
    """

    scatter_plot = alt.Chart(dataFrame).mark_circle(size=10).encode(
        x=alt.X('mixa_pasteur_temp:Q', 
                scale = alt.Scale(
                    domain=[dataFrame['mixa_pasteur_temp'].min() - 10, 
                            dataFrame['mixa_pasteur_temp'].max() + 10]), 
                axis = alt.Axis(title='A살균기의 살균 온도')),
        y=alt.Y('mixb_pasteur_temp:Q', scale = alt.Scale(
            domain=[dataFrame['mixb_pasteur_temp'].min() - 5, 
                    dataFrame['mixb_pasteur_temp'].max() + 5]), 
                axis = alt.Axis(title='B살균기의 살균 온도')),
        color='insp',
        tooltip=['mixa_pasteur_temp', 'mixb_pasteur_temp'],
        
        #color = alt.Color('Origin', range=col)
    ).properties(width=500, height=160).interactive()

    return scatter_plot



def outputChart(chart : alt.vegalite.v4.api.Chart):

    return chart.to_json()
