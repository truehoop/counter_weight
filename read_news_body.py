#-*- coding:utf-8 -*-

# 전처리 과정 'Form Data' 복사해서 사전타입으로 정리
lines = '''byLine: 
categoryCodes: []
dateCodes: []
endDate: 2019-11-12
incidentCodes: []
indexName: news
isNotTmUsable: false
isTmUsable: false
mainTodayPersonYn: 
networkNodeType: 
newsIds: null
providerCodes: []
resultNumber: 10
searchFilterType: 1
searchKey: 삼성 최순실
searchKeys: [{}]
searchScopeType: 1
searchSortType: date
sortMethod: date
startDate: 2019-08-12
startNo: 1
topicOrigin: 
'''.splitlines()

data = {}
for line in lines:
    key, value = line.split(':', 1)
    value = value.strip()
    if value == 'null':
        value = None
    data[key] = value
    print(key, value)

data = {
"byLine": "",
"categoryCodes": [],
"dateCodes": [],
"endDate": "2019-11-12",
"incidentCodes": [],
"indexName": "news",
"isNotTmUsable": 'false',
"isTmUsable": 'false',
"mainTodayPersonYn": "",
"networkNodeType": "",
"newsIds": None,
"providerCodes": [],
"resultNumber": 10,
"searchFilterType": "1",
"searchKey": "삼성 최순실",
"searchKeys": [{}],
"searchScopeType": "1",
"searchSortType": "date",
"sortMethod": "date",
"startDate": "2019-08-12",
"startNo": 12,
"topicOrigin": ""
}

import requests
import json
from bs4 import BeautifulSoup

result_url = "https://www.kinds.or.kr/api/news/search.do"
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Host": "www.kinds.or.kr",
    "Origin": "http://www.kinds.or.kr",
    "Referer": "http://www.kinds.or.kr/v2/news/index.do",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

print(result_url)
#print(data)
print(json.dumps(data, ensure_ascii = False))
body = json.dumps(data, ensure_ascii = False).encode('utf-8')
print(headers)
response = requests.post(result_url, data=body, headers=headers)
print(response)

html = response.text
soup = BeautifulSoup(html, 'html.parser')

print(response.text)
res = response.json()
print(res)
print(res['totalCount'])

# for tag in soup.select('.resultList li h3'):
#     doc_id = tag['id'].replace('news_', '')
#     doc_url = f'https://www.bigkinds.or.kr/news/detailView.do?docId={doc_id}&returnCnt=1'
#     print(tag.text.strip(), doc_url)


# import pymysql
# from dotenv import load_dotenv
# load_dotenv()

# import os

# # Establish a MySQL connection
# db_url = os.environ['DB_URL']
# db_user = os.environ['DB_USER']
# db_password = os.environ['DB_PASSWORD']
# db_name = os.environ['DB_NAME']
# database = pymysql.connect (db_url, db_user, db_password, db_name)
# print(f'Now you gonna Connect to {db_url}')

# # Get the cursor, which is used to traverse the database, line by line
# cursor = database.cursor()

# # Create the INSERT INTO sql query
# query = """INSERT INTO news_data_all (id, news_date, media_name, writer, title, key1, key2, key3, acident1, acident2, acident3, `character`, location, agency, keyword, keyword_export, sentence, url, exception) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE duplication = VALUES(duplication) + 1"""

# book = xlrd.open_workbook(file_name)
# sheet = book.sheet_by_name("sheet")
# cursor = database.cursor()

# max_length = 0
# for r in range(1, sheet.nrows):
#     id  = sheet.cell(r,0).value
#     news_date   = sheet.cell(r,1).value
#     media_name  = sheet.cell(r,2).value
#     writer  = sheet.cell(r,3).value
#     title   = sheet.cell(r,4).value
#     key1    = sheet.cell(r,5).value
#     key2    = sheet.cell(r,6).value
#     key3    = sheet.cell(r,7).value
#     acident1    = sheet.cell(r,8).value
#     acident2    = sheet.cell(r,9).value
#     acident3    = sheet.cell(r,10).value
#     character   = sheet.cell(r,11).value
#     location    = sheet.cell(r,12).value
#     agency  = sheet.cell(r,13).value
#     keyword = sheet.cell(r,14).value
#     keyword_export  = sheet.cell(r,15).value
#     sentence    = sheet.cell(r,16).value
#     url = sheet.cell(r,17).value
#     exception    = sheet.cell(r,18).value

#     # Assign values from each row
#     values = (id, news_date, media_name, writer, title, key1, key2, key3, acident1, acident2, acident3, character, location, agency, keyword, keyword_export, sentence, url, exception)

#     length = len(keyword)
#     if max_length < length:
#         max_length = length
#     # Execute sql Query
#     cursor.execute(query, values)

# print(max_length)
# # Close the cursor
# cursor.close()
# # Commit the transaction
# database.commit()
# print(file_name, 'Done !')

# # Close the database connection
# database.close()