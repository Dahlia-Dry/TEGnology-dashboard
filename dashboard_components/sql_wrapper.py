import pymysql
import pandas as pd
from decouple import config



conn =  pymysql.connect(host=config('AWS_SQL_ENDPOINT'), user=config('AWS_SQL_USER'), passwd=config('AWS_SQL_PASSWORD'), port=3306, database='sensors')
cur = conn.cursor()
def dump_df():
    df= pd.read_csv('temp2.csv',index_col=None)
    for i in range(len(df)):
        sql =  f"INSERT INTO watteco_temp_2 (`timestamp`,`temp1`,`temp2`) VALUES ('{df['timestamp'].iloc[i]}',{df['temp1'].iloc[i]},{df['temp2'].iloc[i]})"
        cur.execute(sql)
        conn.commit()

#sql = 'DROP TABLE abb'
sql = 'CREATE TABLE abb(timestamp datetime, counter int, statusflag int, temp1 int, temp2 int, current1 int, current2 int)'
cur.execute(sql)
cur.execute('SELECT * FROM abb ORDER BY timestamp DESC')
results = cur.fetchmany(10)
print(results)