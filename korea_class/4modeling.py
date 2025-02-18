###################################################
# 엑셀에서 라벨링 결과 import
###################################################

import read_data_from_xslx
eval_result = read_data_from_xslx.get_sheet_value()

###################################################
# 데이터베이스 설정 가져오기
###################################################
import pymysql
from dotenv import load_dotenv
load_dotenv()

###################################################
# 데이터베이스 연결
###################################################
import os
from utils.time import now_ms_ts
import db_connection

# db_connection.connection()
database = db_connection.connect()

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# 데이터베이스 조회 쿼리
query = "select news_date, title, body from manjum.news_data where keyword like '%삼성%' order by news_date limit 300 "
query2 = "select news_date, title, body, valid from manjum.news_data where valid > 0 and valid < 4 order by news_date limit 300"
# 우리가 진짜 쓸 쿼리
query3 = "select id, news_date, title, body, valid from manjum.news_data order by id "

try:
    cursor.execute(query3)
except Exception as e:
    print('e={}, trace={}'.format(repr(e), traceback.format_exc()))

rows = cursor.fetchall()
print("rows", len(rows))
print("eval_result", len(eval_result))

data = []
for row in rows:
    if row[0] in eval_result.keys():
        data.append((row[0], row[1], row[2], row[3], eval_result[row[0]]))

length = len(data)
train_data = data[:int(length*3/4)]
test_data = data[int(length*3/4):]
print(f"총 {length}개의 기사를 불러왔습니다.")

cursor.close()
# Commit the transaction
database.commit()
# Close the database connection
database.close()

###################################################
# 전처리 - 형태소 분석
###################################################

# 불용어
stopwords=['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다', 'br', '/><', '/>', '.<']

from konlpy.tag import Kkma, Okt
from konlpy.utils import pprint

kkma = Kkma()
okt = Okt()

test_nouns = kkma.nouns(rows[1][3])

before_analyze_text = now_ms_ts()
all_nouns = []
all_nouns2 = []
for row in train_data:
    temp_X = okt.morphs(row[3], stem=True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    all_nouns.append(temp_X)

for row in test_data:
    temp_X = okt.morphs(row[3], stem=True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    all_nouns2.append(temp_X)

print('기사 분석에 걸린 시간 : ', now_ms_ts() - before_analyze_text)
print('기사 분석 끝!')
print('첫 번째 기사 토큰', all_nouns[1])

###################################################
# 전처리 - 텍스트를 토큰화
###################################################

from keras.preprocessing.text import Tokenizer
import json

max_words = 10000
tokenizer = Tokenizer(num_words = max_words)
tokenizer.fit_on_texts(all_nouns)

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H-%M-%S")
outputfilename = 'all_nouns' + current_time + '.json'

with open(outputfilename, 'w') as outfile:
    json.dump(all_nouns, outfile)

X_train = tokenizer.texts_to_sequences(all_nouns)
X_test = tokenizer.texts_to_sequences(all_nouns2)

print("본문의 최대 길이 : ", max(len(l) for l in X_train))
print("본문의 평균 길이 : ", sum(map(len, X_train))/ len(X_train))

import matplotlib.pyplot as plt
plt.hist([len(s) for s in X_train], bins=50)
plt.xlabel('length of Data')
plt.ylabel('number of Data')
# plt.show()

import numpy as np
y_train = []
y_test = []

# 결과를 분류할 가짓수
# 1자연생태, 2대기환경, 3수환경, 4토지환경, 5생활환경, 6사회환경ㆍ경제환경

type_of_result = 6

y_result = []
for i in range(type_of_result):
    temp = []
    for j in range(type_of_result):
        if j == i:
            temp.append(1)
        else:
            temp.append(0)
    y_result.append(temp.copy())

for i in range(len(train_data)):
    for type in range(type_of_result):
        if train_data[i][4] == type:
            y_train.append(y_result[type].copy())

for i in range(len(test_data)):
    for type in range(type_of_result):
        if test_data[i][4] == type:
            y_test.append(y_result[type].copy())

y_train = np.array(y_train)
y_test = np.array(y_test)

###################################################
# 모델 만들기
###################################################

from keras.layers import Embedding, Dense, LSTM
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
max_len = 360 # 전체 데이터의 길이를 300으로 맞춘다
X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

model = Sequential()
model.add(Embedding(max_words, 60))
model.add(LSTM(30))
model.add(Dense(type_of_result, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=10, batch_size=10, validation_split=0.1)

res = model.evaluate(X_test, y_test)
print(f"테스트 정확도 : {res[1] * 100}%")

# 예측한 값 비교하기
predict = model.predict(X_test)
predict_labels = np.argmax(predict, axis=1)
original_labels = np.argmax(y_test, axis=1)
for i in range(50):
    print("기사제목 : ", test_data[i][2], "/\t 원래 라벨 : ", original_labels[i], "/\t예측한 라벨 : ", predict_labels[i])

model.save('lstm_model_yn_'+ current_time + '.h5')

