#-*- coding:utf-8 -*-

import requests
import json
import traceback
import copy

from bs4 import BeautifulSoup
import asyncio
import aiohttp
from utils.time import now_ms_ts

import pymysql
from dotenv import load_dotenv
load_dotenv()

import os

import read_data_from_xslx

eval_result = read_data_from_xslx.get_sheet_value()

from utils.time import now_ms_ts
import db_connection

# db_connection.connection()
database = db_connection.connect()

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

query = """select * from analyzer_news"""
try:
    cursor.execute(query)
except Exception as e:
    print('e={}, trace={}'.format(repr(e), traceback.format_exc()))

rows = cursor.fetchall()
print("rows", len(rows))
print("eval_result", len(eval_result))

count = 0
for row in rows:
    if row[0] in eval_result.keys():
        count = count + 1

print(count)

# Create the INSERT INTO sql query
query = """UPDATE manjum.analyzer_news SET valid = %s where id = %s"""

def update_news_to_db(news_update_list):
    before_query = now_ms_ts()

    print(len(news_update_list))

    for key in news_update_list:
        # print(key)
        if key == None:
            continue
        # print(key_data['TITLE'])
        id          = key
        value       = news_update_list[key]
        
        values = (value, id)
        
        if id == '':
            print(values)
        try:
            cursor.execute(query, values)
            print(query, values)
            pass
        except Exception as e:
            print('e={}, trace={}'.format(repr(e), traceback.format_exc()))


    # Close the cursor
    cursor.close()
    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()

    print('db insert time :', now_ms_ts() - before_query)

async def print_when_done():
    update_news_to_db(eval_result)

loop = asyncio.get_event_loop()
loop.run_until_complete(print_when_done())
loop.close()