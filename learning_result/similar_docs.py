import pandas as pd

from gensim.models.doc2vec import Doc2Vec

import os 
import boto3

import pymysql
from dotenv import load_dotenv 

# env 파일 업로드
load_dotenv()

access_key = os.getenv("AWS_KEY")
secret_key = os.getenv("AWS_SECRET_KEY")

# s3 객체 정의.
s3 = boto3.resource('s3',
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key)

bucket = s3.Bucket('hangle-square')
model_file = 'recsys_model/review_d2v.model'
local_model_path = 'review_d2v.model'
bucket.download_file(model_file, local_model_path)

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

# 데이터 로드
news_data = pd.read_sql_query("select * from News ",conn)
conn.close()

# 데이터 전처리
news_data['document'] = news_data['title'] + ' ' + news_data['contents']
news_data['label'] = news_data['keyword'].map({'연예': 0, '스포츠': 1, '정치': 2, '국제': 3, '사회': 4, '문화': 5})
news_data = news_data.dropna(how='any')

# Doc2Vec 모델 로드
model = Doc2Vec.load('review_d2v.model')

# print(f"뉴스 데이터 프레임 {news_data[:5]}")

# 추천 할 문서 갯수 선정
num_recommendations = 5

# 추천할 문서 선택 (데이터프레임의 index 기준으로)
consumed_doc_idx = 10000

# 선택한 문서를 기반으로 유사한 문서들 추천
similar_docs = model.dv.most_similar(consumed_doc_idx, topn=num_recommendations)
# 결과 리스트 추출 
print(similar_docs)

for doc_idx, sim in similar_docs:
        row = news_data.iloc[int(doc_idx)]
        doc_title = row['title']
        doc_keyword = row['keyword']
        doc_content = row['contents']
        doc_date = row['date']
        print(f"유사도: {sim} \n, 제목: {doc_title} \n, 카테고리: {doc_keyword} \n, 본문: {doc_content} \n, 날짜: {doc_date}")
    
# 유사한 문서 번호만 추출후 list에 저장 
reclist = []

for doc_idx, sim in similar_docs:
    reclist.append(doc_idx)
    print(sim)

print(reclist)
