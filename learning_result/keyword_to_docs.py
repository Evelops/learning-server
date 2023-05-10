import pandas as pd
from konlpy.tag import Mecab
from gensim.models.doc2vec import Doc2Vec
import numpy as np

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
news_data = pd.read_sql_query("select * from News",conn)

conn.close()

# 데이터 전처리
news_data['document'] = news_data['title'] + ' ' + news_data['contents']
news_data['label'] = news_data['keyword'].map({'연예': 0, '스포츠': 1, '정치': 2, '국제': 3, '사회': 4, '문화': 5})
news_data = news_data.dropna(how='any')


def recommend_documents(keyword, n=5):
    mecab = Mecab()
    model = Doc2Vec.load("review_d2v.model")

    # 입력된 키워드를 형태소 분석하여 doc2vec 모델에서 유사한 벡터 추출 (mecab 형태소 분석 모델 사용)
    keyword_vector = model.infer_vector(mecab.morphs(keyword))

    # 모든 문서와의 유사도 계산 
    doc_vectors = [model.dv[str(i)] for i in range(len(model.dv))]
    # numpy 모듈의 np.dot() 메서드를 사용하여 학습된 모든 문서 벡터 + 입력된 키워드간 내적 계산 
    similarities = np.dot(doc_vectors, keyword_vector)

    # 상위 n(5)개 문서 추출하여 반환
    top_n_indices = np.argsort(similarities)[::-1][:n]
    recommended_documents = pd.DataFrame(news_data.iloc[top_n_indices])
    return recommended_documents
  
#키워드 '북한'을 입력시 입력한 키워드와 학습된 모든 문서 벡터를 기반으로 유사한 문서 추천 테스트
recommend_documents('북한')