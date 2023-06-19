#-*- coding:utf-8 -*-

from db.connection import Connection
import pandas as pd
import datetime as dt
import numpy as np

db = Connection()
cur = db.conn.cursor()
query="""select std_dt, mixa_pasteur_temp, mixb_pasteur_temp, insp 
   from (select std_dt, mixa_pasteur_temp * 0.1 as mixa_pasteur_temp, 
                mixb_pasteur_temp * 0.1 as mixb_pasteur_temp, 
                insp as insp
	     from data
	     where (mixa_pasteur_state = '0' OR mixa_pasteur_state = '1') AND 
               (mixb_pasteur_state = '0' OR mixb_pasteur_state = '1')) as sub
   where mixa_pasteur_temp IS NOT NULL AND 
	     mixb_pasteur_temp IS NOT NULL
   order by std_dt asc;
"""

sql ="""
select std_dt, mixa_pasteur_temp * 0.1 as mixa_pasteur_temp,  
mixb_pasteur_temp * 0.1 as mixb_pasteur_temp, insp 
from test_data
where mixb_pasteur_state is not null
	and mixa_pasteur_state is not null
	and mixa_pasteur_state < 2
	and mixb_pasteur_state < 2
order by std_dt asc;
"""

try:
    trend_data = pd.read_sql(query, db.conn)

except Exception as e:
    print('Failed to send Query !!!')
    print(e)


def get_Date_Series(start_date: str, end_date: str)-> pd.core.series.Series:
    """
    Return Date's series to Controller
    """

    date_series = trend_data[(trend_data['std_dt'] >= start_date) & 
                             (trend_data['std_dt'] <= end_date)]
    return date_series['std_dt']



def get_Y_Series(start_date: str, end_date: str, y_label: str)-> pd.core.series.Series: 
    """
    Return y_label's series to Controller
    """

    y_series = trend_data[(trend_data['std_dt'] >= start_date) & 
                          (trend_data['std_dt'] <= end_date)]
    y_series = np.round(y_series, 2)

    return y_series[y_label]

