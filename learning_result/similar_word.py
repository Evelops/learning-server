from gensim.models import KeyedVectors
import boto3 
import os 
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
model_file = 'recsys_model/review_w2v'
local_model_path = 'review_w2v_test'
bucket.download_file(model_file, local_model_path)

# 모델 로드
try:
    loaded_model = KeyedVectors.load_word2vec_format(local_model_path)
except KeyError:
    print("모델 로드 X ")

# 모델 로드
try:
    # loaded_model = KeyedVectors.load_word2vec_format("review_w2v")
    model_result = loaded_model.most_similar("한국")
    for res in model_result:
        word, score = res
        print(f"({word}, {score})\n")
except KeyError:
    print("입력된 단어에 대한 유사 단어를 찾을 수 없습니다. ")