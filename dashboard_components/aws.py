
import pymysql



def test():
    from decouple import config
    #connect_to_bucket(config('AWS_ACCESS_KEY_ID'),config('AWS_SECRET_ACCESS_KEY'),'watteco-temp2')

    host = 'tegnology.cvdmv6p7tm4s.eu-north-1.rds.amazonaws.com'
    AWS_SQL_USER = 'tegnology'
    AWS_SQL_PASSWORD = 'TEGnology2023!'
    database = 'watteco_temp_2'
    region = 'eu-north-1'
    
    #session = boto3.Session(aws_access_key_id=config('AWS_ACCESS_KEY_ID'),aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),region_name='eu-north-1')
    #client = session.client('rds')
    #token = client.generate_db_auth_token(DBHostname=host, Port=3306, DBUsername=AWS_SQL_USER, Region=region)
    #print(token)
    conn =  pymysql.connect(host=host, user=AWS_SQL_USER, passwd=AWS_SQL_PASSWORD, port=3306, database=database)
    try:
        
        cur = conn.cursor()
        cur.execute('SELECT * FROM data')
        results = cur.fetchmany(10)
        print(results)
    except Exception as e:
        print("Database connection failed due to {}".format(e))  
    # connection = pymysql.connect(host=host, 
    #                              user=AWS_SQL_USER, 
    #                              password=AWS_SQL_PASSWORD, 
    #                              port=3306,
    #                              database=database,
    #                              charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor)
    # cur = connection.cursor()
    # sql = "CREATE TABLE data(timestamp varchar(255),temp1 float,temp2 float);"
    # #sql = "INSERT INTO data (`timestamp`,`temp1`,`temp2`) VALUES ('09/17/2023 09:47:47 pm',17.2,20.6)"
    # cur.execute(sql)
    # connection.commit()
    #cur.execute('SELECT * FROM data')
    #results = cur.fetchmany(3)
    #print(results)




test()