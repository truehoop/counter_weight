
import pymysql
from dotenv import load_dotenv
load_dotenv()

import os
from utils.time import now_ms_ts
import db_connection

# db_connection.connection()
database = db_connection.connect()

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
query = "select news_date, title, body from manjum.analyzer_news where keyword like '%삼성%' order by news_date limit 300 "
query2 = "select news_date, title, body, valid from manjum.analyzer_news where valid > 0 and valid < 4 order by news_date limit 300"

try:
    cursor.execute(query2)
except Exception as e:
    print('e={}, trace={}'.format(repr(e), traceback.format_exc()))

rows = cursor.fetchall()
length = len(rows)
train_data = rows[:int(length/2)]
test_data = rows[int(length/2):]
print(f"총 {length}개의 기사를 불러왔습니다.")

cursor.close()
# Commit the transaction
database.commit()
# Close the database connection
database.close()

###################################################
# 전처리
###################################################

# 불용어
stopwords=['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

from konlpy.tag import Kkma
from konlpy.utils import pprint

kkma = Kkma()

test_nouns = kkma.nouns(rows[1][2])

before_analyze_text = now_ms_ts()
all_nouns = []
all_nouns2 = []
for row in train_data:
    current_nouns = kkma.nouns(row[2])
    all_nouns.append(current_nouns)

for row in test_data:
    current_nouns = kkma.nouns(row[2])
    all_nouns2.append(current_nouns)

print(now_ms_ts() - before_analyze_text)
print('기사 분석 끝!')

from keras.preprocessing.text import Tokenizer

max_words = 35000
tokenizer = Tokenizer(num_words = max_words)
tokenizer.fit_on_texts(all_nouns)

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
for i in range(len(train_data)):
    if train_data[i][3] == 1:
        y_train.append([1, 0, 0])
    elif train_data[i][3] == 2:
        y_train.append([0, 1, 0])
    elif train_data[i][3] == 3:
        y_train.append([0, 0, 1])
    elif train_data[i][3] == 4:
        y_train.append([0, 0, 0])
for i in range(len(test_data)):
    if test_data[i][3] == 1:
        y_test.append([1, 0, 0])
    elif test_data[i][3] == 2:
        y_test.append([0, 1, 0])
    elif test_data[i][3] == 3:
        y_test.append([0, 0, 1])
    elif test_data[i][3] == 4:
        y_test.append([0, 0, 0, 1])

y_train = np.array(y_train)
y_test = np.array(y_test)

###################################################
# 모델 만들기
###################################################

from keras.layers import Embedding, Dense, LSTM
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
max_len = 300 # 전체 데이터의 길이를 20로 맞춘다
X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

model = Sequential()
model.add(Embedding(max_words, 100))
model.add(LSTM(128))
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=10, batch_size=10, validation_split=0.1)

res = model.evaluate(X_test, y_test)
print(f"테스트 정확도 : {res[1] * 100}%")

# 예측한 값 비교하기
predict = model.predict(X_test)
import numpy as np
predict_labels = np.argmax(predict, axis=1)
original_labels = np.argmax(y_test, axis=1)
for i in range(30):
    print("기사본문 : ", test_data[i][1], "/\t 원래 라벨 : ", original_labels[i], "/\t예측한 라벨 : ", predict_labels[i])


exit()

# from keras.layers import Embedding

# Embedding 층은 적어도 두 개의 매개변수를 받습니다.
# 가능한 토큰의 개수(여기서는 1,000으로 단어 인덱스 최댓값 + 1입니다)와 임베딩 차원(여기서는 64)입니다
# 인덱스는 0을 사용하지 않으므로 단어 인덱스는 1~999사이의 정수입니다
# embedding_layer = Embedding(1000, 64)

from tensorflow.keras.datasets import reuters


reuter_data = reuters.load_data(num_words=None, test_split=0.2)
print(reuter_data)

(X_train, y_train), (X_test, y_test) = reuters.load_data(num_words=None, test_split=0.2)

print('훈련용 뉴스 기사 : {}'.format(len(X_train)))
print('테스트용 뉴스 기사 : {}'.format(len(X_test)))
num_classes = max(y_train) + 1
print('카테고리 : {}'.format(num_classes))

print(X_train[0]) # 첫번째 훈련용 뉴스 기사
print(y_train[0]) # 첫번째 훈련용 뉴스 기사의 레이블

import pandas as pd
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

apple_training_complete = pd.read_csv(r'E:\Datasets\apple_training.csv')
apple_training_processed = apple_training_complete.iloc[:, 1:2].values

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0, 1))

apple_training_scaled = scaler.fit_transform(apple_training_processed)

features_set = []
labels = []
for i in range(60, 1260):
    features_set.append(apple_training_scaled[i-60:i, 0])
    labels.append(apple_training_scaled[i, 0])

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(features_set.shape[1], 1)))

model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50))
model.add(Dropout(0.2))

model.add(Dense(units=1))

model.compile(optimizer = 'adam', loss = 'mean_squared_error')
model.fit(features_set, labels, epochs=100, batch_size=32)

apple_testing_complete = pd.read_csv(r'E:\Datasets\apple_testing.csv')
apple_testing_processed = apple_testing_complete.iloc[:, 1:2].values

apple_total = pd.concat((apple_training_complete['Open'], apple_testing_complete['Open']), axis=0)

test_inputs = apple_total[len(apple_total) - len(apple_testing_complete) - 60:].values
test_inputs = test_inputs.reshape(-1,1)
test_inputs = scaler.transform(test_inputs)

test_features = []
for i in range(60, 80):
    test_features.append(test_inputs[i-60:i, 0])


test_features = np.array(test_features)
test_features = np.reshape(test_features, (test_features.shape[0], test_features.shape[1], 1))


# Making Predection

predictions = model.predict(test_features)

predictions = scaler.inverse_transform(predictions)

plt.figure(figsize=(10,6))
plt.plot(apple_testing_processed, color='blue', label='Actual Apple Stock Price')
plt.plot(predictions , color='red', label='Predicted Apple Stock Price')
plt.title('Apple Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Apple Stock Price')
plt.legend()
plt.show()


