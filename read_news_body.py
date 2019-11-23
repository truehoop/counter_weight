#-*- coding:utf-8 -*-

import requests
import json
import traceback
import copy

from bs4 import BeautifulSoup
import asyncio
import aiohttp
from utils.time import now_ms_ts

# 전처리 과정 'Form Data' 복사해서 사전타입으로 정리
lines = '''byLine: 
categoryCodes: []
dateCodes: []
endDate: 2019-11-20
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
    # print(key, value)

data = {
"byLine": "",
"categoryCodes": [],
"dateCodes": [],
"endDate": "2019-11-20",
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
# "searchKey": "삼성 최순실",
"searchKey": "(삼성 OR 신세계 OR 현대 OR SK OR LG OR 롯데 OR 포스코 OR 한화 OR GS OR 농협 OR KT) AND (가계빈곤 OR 경제노출 OR 경제충격 OR 근로빈곤층 OR 기아 OR 기초생활 OR 기초생활보장 OR 남성빈곤 OR 노인빈곤 OR 노인일자리 OR 미달가구 OR 보험 OR 빈곤 OR 빈곤인구 OR 빈곤층 OR 사각지대 OR 사회노출 OR 사회보장 OR 사회보장제도 OR 사회서비스 OR 사회안전망 OR 사회충격 OR 생계 OR 성별빈곤 OR 소득 OR 실업급여 OR 여성빈곤 OR 영양실조 OR 의료 OR 이주민빈곤 OR 장애빈곤 OR 재난 OR 재난노출 OR 주거 OR 청년빈곤 OR 청소년빈곤 OR 최저주거 OR 취약계층 OR 환경노출 OR 환경충격)",
"searchKeys": [{}],
# "searchKeys": [{"orKeywords": ["삼성, 신세계, 현대, SK,LG"]}],
"searchScopeType": "2",
"searchSortType": "date",
"sortMethod": "date",
"startDate": "2018-11-20",
"startNo": 1,
"topicOrigin": ""
}

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

print(json.dumps(data, ensure_ascii = False))
body = json.dumps(data, ensure_ascii = False).encode('utf-8')
print(headers)
loop = asyncio.get_event_loop()
count = 0

async def fetch_post(session, url, body):
    try:
        async with session.post(url, json=body, headers=headers) as response:
            res = await response.json()
            return res
    except Exception as e:
        print('e={}, trace={}'.format(repr(e), traceback.format_exc()))

async def fetch_get(session, url, result):
    try:
        async with session.post(url, headers=headers) as response:
            res = await response.json()
            return res
    except Exception as e:
        print('e={}, trace={}'.format(repr(e), traceback.format_exc()))
        print(result)

def read_news_detail(session, res):
    before_read_list = now_ms_ts()
    tasks = []

    for result in res['resultList']:
        # print(result)
        # print(result['NEWS_ID'])
        news_url = f"https://www.bigkinds.or.kr/news/detailView.do?docId={result['NEWS_ID']}&returnCnt=1&sectionDiv=1000"
        # response = await fetch_get(session, news_url)
        tasks.append(fetch_get(session, news_url, result))
        # response = requests.get(news_url, data=body, headers=headers)
        # print(response)
        global count
        count = count + 1
        # if count > 100:
        #     break
        if count % 1000 == 0:
            print(count)
        # print(response['detail']['TITLE'])
    # news_list = await asyncio.gather(*tasks)
    return tasks
    print('Every 10 post', now_ms_ts() - before_read_list)

async def post_news_list():
    tasks = []
    async with aiohttp.ClientSession() as session:
        first_call = await fetch_post(session, result_url, data)
        print('totalCount: ', first_call['totalCount'])
        for index in range(1, int((first_call['totalCount']+9)/10)):
            data['startNo'] = index
            temp_data = copy.copy(data)
            tasks.append(fetch_post(session, result_url, temp_data))
        
        before_read_news_detail = now_ms_ts()
        news_list = await asyncio.gather(*tasks)
        print('뉴스 리스트 호출 시 걸린 시간 :', now_ms_ts() - before_read_news_detail)
        detail_tasks = []
        for news in news_list:
            detail_list = read_news_detail(session, news)
            detail_tasks.extend(detail_list)
        
        news_detail_list = await asyncio.gather(*detail_tasks)
        
        print('전체 호출 시 걸린 시간 :', now_ms_ts() - before_read_news_detail)

        return news_detail_list
            # print(news_detail['detail']['TITLE'])
    # response = requests.post(result_url, data=body, headers=headers)
    # print(response)

    # res = response.json()
    # print(res)
    # print(res['totalCount'])
    # print(res['resultList'])

# def parsing(response):
#     html = response.text
#     soup = bs4(html, 'html.parser')
#     print(response.text)

# for tag in soup.select('.resultList li h3'):
#     doc_id = tag['id'].replace('news_', '')
#     doc_url = f'https://www.bigkinds.or.kr/news/detailView.do?docId={doc_id}&returnCnt=1'
#     print(tag.text.strip(), doc_url)


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

if os.environ['DB_USE_LOCAL'] == False:
    db_url = os.environ['DB_URL']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_port = 3306
    db_name = os.environ['DB_NAME']

database = pymysql.connect (host=db_url, port=db_port, user=db_user, passwd=db_password, db='mysql')
print(f'Now you gonna Connect to {db_url}')

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
query = """INSERT INTO manjum.news_data_all (id, news_date, media_name, writer, title, key1, key2, key3, acident1, acident2, acident3, `character`, location, agency, keyword, keyword_export, url, exception, body) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE duplication = VALUES(duplication) + 1"""

def insert_news_to_db(news_detail_list):
    before_query = now_ms_ts()

    print(len(news_detail_list))

    for detail in news_detail_list:
        # print(detail)
        detail_data = detail['detail']
        # print(detail_data['TITLE'])
        id          = detail_data['NEWS_ID']
        news_date   = detail_data['DATE']
        media_name  = detail_data['PROVIDER']
        writer      = detail_data['BYLINE']
        title       = detail_data['TITLE']
        key         = detail_data['CATEGORY'].split('|')
        key1        = key[0] if len(key) > 0 else ''
        key2        = key[1] if len(key) > 1 else ''
        key3        = key[2] if len(key) > 2 else ''
        acident     = detail_data['CATEGORY_INCIDENT'].split('|')
        acident1    = acident[0] if len(acident) > 0 else ''
        acident2    = acident[1] if len(acident) > 1 else ''
        acident3    = acident[2] if len(acident) > 2 else ''
        character   = detail_data['TMS_NE_PERSON']
        location    = detail_data['TMS_NE_LOCATION']
        agency      = detail_data['TMS_NE_ORGANIZATION']
        keyword     = detail_data['TMS_RAW_STREAM']
        keyword_export= detail_data['TMS_NE_STREAM']
        url         = detail_data['PROVIDER_LINK_PAGE']
        exception   = ''
        body        = detail_data['CONTENT']
        
        values = (id, news_date, media_name, writer, title, key1, key2, key3, acident1, acident2, acident3, character, location, agency, keyword, keyword_export, url, exception, body)
        
        if title == '' or writer == '' or id == '' or media_name == '':
            print(values)
        try:
            cursor.execute(query, values)
        except Exception as e:
            print('e={}, trace={}'.format(repr(e), traceback.format_exc()))


    # Close the cursor
    cursor.close()
    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()

    print('db insert time :', now_ms_ts() - before_query)

async def print_when_done(tasks):
    for res in asyncio.as_completed(tasks):
        news_detail_list = await res
        insert_news_to_db(news_detail_list)

coros = [post_news_list()]
loop = asyncio.get_event_loop()
loop.run_until_complete(print_when_done(coros))
loop.close()