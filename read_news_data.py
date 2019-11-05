file_name = 'news_data_all/ALLcompany_1.xlsx'

# import pandas as pd

# xl_file = pd.ExcelFile(file_name)

# dfs = {sheet_name: xl_file.parse(sheet_name) 
#           for sheet_name in xl_file.sheet_names}

# for item in dfs.items():
#     print(item)


import xlrd
import pymysql
from dotenv import load_dotenv
load_dotenv()

import os

# Establish a MySQL connection
db_url = os.environ['DB_URL']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
database = pymysql.connect (db_url, db_user, db_password, db_name)
print(f'Now you gonna Connect to {db_url}')

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
query = """INSERT INTO news_data_all (id, news_date, media_name, writer, title, key1, key2, key3, acident1, acident2, acident3, `character`, location, agency, keyword, keyword_export, sentence, url, exception) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE duplication = VALUES(duplication) + 1"""

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for i in range(3, 17):
    file_name = f'news_data_all/ALLcompany_{i}.xlsx'
    print(file_name)
    # Open the workbook and define the worksheet
    book = xlrd.open_workbook(file_name)
    sheet = book.sheet_by_name("sheet")
    cursor = database.cursor()

    max_length = 0
    for r in range(1, sheet.nrows):
        id  = sheet.cell(r,0).value
        news_date   = sheet.cell(r,1).value
        media_name  = sheet.cell(r,2).value
        writer  = sheet.cell(r,3).value
        title   = sheet.cell(r,4).value
        key1    = sheet.cell(r,5).value
        key2    = sheet.cell(r,6).value
        key3    = sheet.cell(r,7).value
        acident1    = sheet.cell(r,8).value
        acident2    = sheet.cell(r,9).value
        acident3    = sheet.cell(r,10).value
        character   = sheet.cell(r,11).value
        location    = sheet.cell(r,12).value
        agency  = sheet.cell(r,13).value
        keyword = sheet.cell(r,14).value
        keyword_export  = sheet.cell(r,15).value
        sentence    = sheet.cell(r,16).value
        url = sheet.cell(r,17).value
        exception    = sheet.cell(r,18).value

        # Assign values from each row
        values = (id, news_date, media_name, writer, title, key1, key2, key3, acident1, acident2, acident3, character, location, agency, keyword, keyword_export, sentence, url, exception)

        length = len(keyword)
        if max_length < length:
            max_length = length
        # Execute sql Query
        cursor.execute(query, values)

    print(max_length)
    # Close the cursor
    cursor.close()
    # Commit the transaction
    database.commit()
    print(file_name, 'Done !')

# Close the database connection
database.close()

# Print results
print ("All Done! Bye, for now.")
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print (f'I just imported{columns} columns and {rows} rows to MySQL!')