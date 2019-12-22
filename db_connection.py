
import pymysql
from dotenv import load_dotenv
load_dotenv()
import os
import sqlalchemy

# Establish a MySQL connection
db_url = os.environ['DB_LOCAL_URL']
db_user = os.environ['DB_LOCAL_USER']
db_password = os.environ['DB_LOCAL_PASSWORD']
db_port = int(os.environ['DB_LOCAL_PORT'])
db_name = os.environ['DB_LOCAL_NAME']

if os.environ['DB_USE_LOCAL'] == 'FALSE':
    db_url = os.environ['DB_URL']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_port = int(os.environ['DB_PORT'])
    db_name = os.environ['DB_NAME']
    db_instance_name = os.environ['DB_INSTANCE_NAME']
    
    engine = sqlalchemy.create_engine(sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        host=db_url,
        username=db_user,
        password=db_password,
        database=db_name,
        query={
            'unix_socket': '/cloudsql/{}'.format(db_instance_name),
            'charset': 'utf8mb4'
        }
    ),
    )
    # database = engine.connect()
    database = connection = pymysql.connect(host='127.0.0.1',
                             user=db_user,
                             password=db_password,
                             port=33066,
                             db='manjum')
    # database = pymysql.connect (host='127.0.0.1', port=33066, user=db_user, passwd=db_password, db='manjum')
else:
    database = pymysql.connect (host=db_url, port=db_port, user=db_user, passwd=db_password, db='mysql')
print(f'Now you gonna Connect to {db_url}')

def connect():
  return database