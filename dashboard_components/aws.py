
import pymysql
import pandas as pd



def test():
    from decouple import config
    #connect_to_bucket(config('AWS_ACCESS_KEY_ID'),config('AWS_SECRET_ACCESS_KEY'),'watteco-temp2')

    host = 'tegnology-ttn-sensors.cvdmv6p7tm4s.eu-north-1.rds.amazonaws.com'
    AWS_SQL_USER = 'tegnology'
    AWS_SQL_PASSWORD = 'TEGnology2023!'
    database = 'sensors'
    region = 'eu-north-1'
    
    #session = boto3.Session(aws_access_key_id=config('AWS_ACCESS_KEY_ID'),aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),region_name='eu-north-1')
    #client = session.client('rds')
    #token = client.generate_db_auth_token(DBHostname=host, Port=3306, DBUsername=AWS_SQL_USER, Region=region)
    #print(token)
    conn =  pymysql.connect(host=host, user=AWS_SQL_USER, passwd=AWS_SQL_PASSWORD, port=3306, database=database)
    cur = conn.cursor()
    df= pd.read_csv('temp2.csv',index_col=None)
    print(df.columns)
    df=df.drop(columns=['Unnamed: 0'])
    for i in range(len(df)):
        sql =  f"INSERT INTO watteco_temp_2 (`timestamp`,`temp1`,`temp2`) VALUES ('{df['timestamp'].iloc[i]}',{df['temp1'].iloc[i]},{df['temp2'].iloc[i]})"
        cur.execute(sql)
        conn.commit()
    cur.execute('SELECT * FROM watteco_temp_2 ORDER BY timestamp DESC')
    results = cur.fetchmany(10)
    print(results)
    



test()