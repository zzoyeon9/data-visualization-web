#-*- coding:utf-8 -*-

from db.connection import Connection
import pandas as pd
import numpy as np
import sys

db = Connection()
cur = db.conn.cursor()
query = """select std_dt, mixa_pasteur_temp, mixb_pasteur_temp
           from (select std_dt, mixa_pasteur_temp * 0.1 as mixa_pasteur_temp, mixb_pasteur_temp * 0.1 as mixb_pasteur_temp
                 from data
                 where (mixa_pasteur_state = '0' OR mixa_pasteur_state = '1') AND
                        (mixb_pasteur_state = '0' OR mixb_pasteur_state = '1')
                        order by std_dt asc) as sub
           where mixa_pasteur_temp IS NOT NULL AND
                 mixb_pasteur_temp IS NOT NULL;
     """
try:
    cur.execute(query)
    df = pd.read_sql(query, db.conn)

except Exception as e:
    print ('Failed to send Query !!!')
    print ("exception : ", e)
    sys.exit(1)

       
def get_MIXA_TEMP(start_date: str, end_date: str, label: str) -> list:
    """
    Return label's list
    """

    spc_df = df[(df['std_dt'] >= start_date) & (df['std_dt'] <= end_date)]
    data_list = spc_df[label].values.tolist()
   
    return data_list
       
