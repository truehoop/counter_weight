# manjum
가치지향적 소비를 위한 기업행동 이력 평가 : 가치지향적 소비의 촉진을 위해 기업 행위를 분석하고 시각화 합니다.

1. 빅카인즈 데이터베이스에서 kSDGs 17개 가치 각각에 해당하는 키워드를을 검색해 기사를 추출합니다.
2. 추출한 기사들의 본문을 크롤링합니다.
3. 크롤링한 본문을 모두 형태소분석하여 머신러닝 모델에 학습시킵니다.
4. LSTM 알고리즘을 사용하여 17가지 가치에 대해서 지도학습을 진행합니다.
5. 같은 알고리즘으로 긍정/부정 2가지에 대해서도 지도학습을 진행합니다.
6. 진행한 모델로 웹 페이지에서 새로운 기사의 가치와 긍정/부정을 조회할 수 있습니다.

## 사용법
env 파일을 생성합니다. 형식은 다음과 같습니다.
```
DB_URL=실서버 DB 주소
DB_USER=실서버 유저 정보
DB_PASSWORD=실서버 비밀번호
DB_NAME=실서버 DB 이름
DB_PORT=실서버 DB 포트
DB_INSTANCE_NAME=실서버 GAE 인스턴스 이름

DB_USE_LOCAL=TRUE

DB_LOCAL_URL=로컬호스트 URL
DB_LOCAL_USER=로컬 유저
DB_LOCAL_PASSWORD=로컬 비밀번호
DB_LOCAL_NAME=로컬 DB 이름
DB_LOCAL_PORT=로컬 포트
```
1. read_news_data로 엑셀 데이터를 DB에 입력합니다.
2. read_news_body로 DB에 있는 뉴스들의 본문을 크롤링합니다.
3. sentiment_analysis로 머신러닝한 결과를 확인합니다.

## 파일 설명
* news_data/, news_data_all/
  * 원문 뉴스 데이터가 포함되어 있습니다.
* read_news_data.py
  * 뉴스 데이터를 읽어서 DB에 저장합니다.
* read_news_body.py
  * 뉴스 본문을 읽어서 DB에 저장합니다.
* sentiment_analysis.py
  * LSTM을 모델을 활용해 가치를 평가하고 긍정 부정을 평가합니다.
* read_data_from_xslx.py
  * 엑셀에서 데이터를 읽어서 필요한 컬럼을 dictionary 형태로 반환합니다.
