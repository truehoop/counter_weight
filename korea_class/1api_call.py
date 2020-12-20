# -*- coding:utf-8 -*-
import requests
import json
from pprint import pprint

# POST BODY
data = {
    "byLine": "",
    "categoryCodes": [],
    "dateCodes": [],
    "endDate": "2020-12-19",  # 끝나는 날짜
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
    # 검색식
    "searchKey": "((삼성 OR 신세계 OR 현대 OR SK OR LG OR 롯데 OR 포스코 OR 한화 OR GS OR 농협 OR KT) AND (가계빈곤 OR 경제노출 OR 경제충격 OR 근로빈곤층 OR 기아 OR 기초생활 OR 기초생활보장 OR 남성빈곤 OR 노인빈곤 OR 노인일자리 OR 미달가구 OR 보험 OR 빈곤 OR 빈곤인구 OR 빈곤층 OR 사각지대 OR 사회노출 OR 사회보장 OR 사회보장제도 OR 사회서비스 OR 사회안전망 OR 사회충격 OR 생계 OR 성별빈곤 OR 소득 OR 실업급여 OR 여성빈곤 OR 영양실조 OR 의료 OR 이주민빈곤 OR 장애빈곤 OR 재난 OR 재난노출 OR 주거 OR 청년빈곤 OR 청소년빈곤 OR 최저주거 OR 취약계층 OR 환경노출 OR 환경충격))",
    "searchKeys": [{}],
    # "searchKeys": [{"orKeywords": ["삼성, 신세계, 현대, SK,LG"]}],
    "searchScopeType": "1",  # 1: 제목검색 2: 제목+내용검색
    "searchSortType": "date",
    "sortMethod": "date",
    "startDate": "2020-09-19",  # 시작날짜
    "startNo": 1,
    "topicOrigin": ""
}
result_url = "https://www.kinds.or.kr/api/news/search.do"
# POST HEADER
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
body = json.dumps(data, ensure_ascii=False).encode('utf-8')

# API 요청
response = requests.post(result_url, data=body, headers=headers)

# 결과 출력
pprint(response.json())
