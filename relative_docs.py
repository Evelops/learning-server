# 기존 word2vec 로 학습한 모델을 doc2vec 기반의 모델로 변경후 d2v 이라는 이름으로 저장
import os 
import io

import ssl
import certifi
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request

import boto3

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from konlpy.tag import Mecab

import pymysql
from dotenv import load_dotenv

from tqdm import tqdm

# s3 객체 정의.
s3_client = boto3.client('s3')

# env 파일 업로드
load_dotenv()
# 환경 변수에서 DB 연결 정보 로드
DB_HOST = os.getenv("N_DB_HOST")
DB_USER = os.getenv("N_DB_USER")
DB_PASSWORD = os.getenv("N_DB_PWD")
DB_NAME = os.getenv("N_DB_NAME")
DB_PORT = os.getenv("DB_PORT")

conn = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    db=DB_NAME,
    charset='utf8'
)
cur = conn.cursor()

# RDS에서 데이터 호출 
train_data = pd.read_sql_query("select * from News",conn)
# train_data = pd.read_csv('news.csv')
print(train_data)

# "title" 열에서 필요없는 문자 제거
train_data["title"] = train_data["title"].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", regex=True)

# "content" 열에서 필요없는 문자 제거
train_data["contents"] = train_data["contents"].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", regex=True)

# idx 행의 값을 재배열  ex) idx 2XXXX -> 1
train_data["idx"] = range(1, len(train_data)+1)

# title, contents 값을 document라는 새로운 컬럼으로 생성
train_data['document'] = train_data['title']+' '+train_data['contents']

#keyword 라는 컬럼을 숫자로 매핑하여 labeling 작업 => 별도로 label이라는 컬럼을 생성하여 적용
train_data['label'] = train_data['keyword'].map({'연애': 0, '스포츠': 1, '정치': 2, '국제': 3, '사회': 4, '문화': 5})

print(train_data)

conn.close()

train_data['document'] = train_data['title']+' '+train_data['contents']
train_data['label'] = train_data['keyword'].map({'연애': 0, '스포츠': 1, '정치': 2, '국제': 3, '사회': 4, '문화': 5})
print(train_data.isnull().values.any())

train_data = train_data.dropna(how='any')
print(len(train_data))

# okt to mecab 
mecab = Mecab()

stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '불펌', '금지', '기사', '기자', '속보']
tagged_data = [TaggedDocument(words=mecab.morphs(_d), tags=[str(i)]) for i, _d in enumerate(tqdm(train_data['document']))]

model = Doc2Vec(tagged_data, vector_size=100, window=5, min_count=5, workers=6, dm=1)
# model.save('model/review_d2v.model')

# model 객체를 바이트 형식으로 직렬화
model_bytes = io.BytesIO()
model.save(model_bytes)
model_bytes.seek(0)
# s3에 저장 
s3_client.upload_fileobj(model_bytes,'hangle-square',"recsys_model/review_d2v.model")