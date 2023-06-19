#-*- coding:utf-8 -*-

from db.connection import Connection
import pandas as pd

db = Connection()
cur = db.conn.cursor()

query="""select std_dt, mixa_pasteur_temp, 
                mixb_pasteur_temp, insp 
         from (select std_dt, mixa_pasteur_temp * 0.1 
                      as mixa_pasteur_temp, 
                      mixb_pasteur_temp * 0.1 
                      as mixb_pasteur_temp, 
                      insp as insp
	           from data
	           where (mixa_pasteur_state = '0' OR 
                      mixa_pasteur_state = '1') AND 
                     (mixb_pasteur_state = '0' OR 
                      mixb_pasteur_state = '1')) as sub
         where mixa_pasteur_temp IS NOT NULL AND 
	           mixb_pasteur_temp IS NOT NULL
         order by std_dt asc;
"""



try:
    df = pd.read_sql(query, db.conn)

except Exception as e:
    print(e)


def getScatterDataFrame(start_date: str, end_date: str):

    scatter_df = df[(df['std_dt'] >= start_date) & 
                    (df['std_dt'] <= end_date)]

    return scatter_df

