import logging
import os

# 현재 작업 디렉토리의 절대 경로를 구함
cwd = os.path.abspath(os.getcwd())

# 로그 파일 경로를 절대 경로로 지정
log_path = os.path.join(cwd, 'example.log')

# 로그 파일 생성
logging.basicConfig(filename=log_path, level=logging.DEBUG)

# 로그 작성
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
