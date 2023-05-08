import os

import ssl
import certifi
import pandas as pd
import urllib.request
from gensim.models.doc2vec import Doc2Vec
from tqdm import tqdm

import pymysql
from dotenv import load_dotenv

# 데이터 로드
news_data = pd.read_csv('news.csv')

# 데이터 전처리
news_data['document'] = news_data['title'] + ' ' + news_data['contents']
news_data['label'] = news_data['keyword'].map({'연애': 0, '스포츠': 1, '정치': 2, '국제': 3, '사회': 4, '문화': 5})
news_data = news_data.dropna(how='any')

# Doc2Vec 모델 로드
model = Doc2Vec.load('review_d2v.model')

# 추천 할 문서 갯수 선정 
num_recommendations = 100

# 추천할 문서 선택 (데이터프레임의 index 기준으로)
consumed_doc_idx = 231

# 선택한 문서 출력
print(news_data['title'].iloc[consumed_doc_idx])
print(news_data['contents'].iloc[consumed_doc_idx])

# 선택한 문서를 기반으로 유사한 문서들 추천
similar_docs = model.dv.most_similar(consumed_doc_idx, topn=num_recommendations)

print(similar_docs)

for doc_idx, sim in similar_docs:
        row = news_data.iloc[int(doc_idx)]
        doc_title = row['title']
        doc_keyword = row['keyword']
        doc_content = row['contents']
        print(f"유사도: {sim} \n, 제목: {doc_title} \n, 카테고리: {doc_keyword} \n, 본문: {doc_content} \n")