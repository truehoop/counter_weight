import pymysql
from dotenv import load_dotenv
load_dotenv()

import os

# Establish a MySQL connection
db_url = os.environ['DB_LOCAL_URL']
db_user = os.environ['DB_LOCAL_USER']
db_password = os.environ['DB_LOCAL_PASSWORD']
db_port = int(os.environ['DB_LOCAL_PORT'])
db_name = os.environ['DB_LOCAL_NAME']

database = pymysql.connect (host=db_url, port=db_port, user=db_user, passwd=db_password, db='mysql')

print(f'Now you gonna Connect to {db_url}')

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
values1 = ('조효진2', '에코시스템의 이해', 'A+')
values2 = ('정효진2', '에코시스템의 이해', 'B+')
values3 = ('이효진2', '에코시스템의 이해', 'C+')

query = """INSERT INTO manjum.test(id, class, grade) VALUES (%s, %s, %s)"""

cursor.execute(query, values1)
cursor.execute(query, values2)
cursor.execute(query, values3)

# Close the cursor
cursor.close()
# Commit the transaction
database.commit()

# Close the database connection
database.close()

print('success !')

