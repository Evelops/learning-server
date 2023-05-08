## recsys learning server 
<hr>
<br>

### konlpy & Mecab 설치 (우분투 학습 서버 기준)

<br>

> Java JDK 설치 
<br>

```bash
$ sudo apt-get install openjdk-8-jdk python-dev python3-dev # jdk 1.8 버전 설치 
$ java -version # jdk 버전확인 
```

> konlpy 설치 
<br>

```bash 
$ sudo pip3 install konlpy jpype1-py3 # konlpy 설치 
```

<br>

> Mecab 설치 

```bash 
$ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh) # 수동 mecab 모듈 설치  

# mecab 설치 경로이동 
$ cd /tmp
$ ls 
# mecab-0.996-ko-0.9.2, mecab-ko-dic-2.1.1-20180720 없을시 아래 1,2번 실행  
# 1
$ curl -LO https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz  
$ tar zxfv mecab-0.996-ko-0.9.2.tar.gz 
# 2 
$ curl -LO https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz
$ tar -zxvf mecab-ko-dic-2.1.1-20180720.tar.gz

# 1,2 모두 설치 후 압축 풀고 다음 실행 
$ /tmp/mecab-ko-dic-2.1.1-20180720
$ sudo ldconfig
$ ldconfig -p | grep /usr/local/lib
```

> Mecab-ko 설치 
<br>

```bash 
$ cd /tmp/mecab-0.996-ko-0.9.2
$ ./configure
$ make
$ make check
$ sudo make install
```

> Mecab-ko-dic 설치 
<br>

```bash 
$ cd /tmp/mecab-ko-dic-2.1.1-20180720
$ ./autogen.sh
$ ./configure
$ make
$ sudo make install
```
<br> 

### 가상화 & 학습  
<br>

> set up venv
<br>

```bash 
sudo apt-get update 
sudo apt-get install python3 python3-venv #install p3-venv
python3 -m venv recsys # recsys 명칭의 폴더 가상화 
```
<br>

> go to venv
<br>

```bash
$ source path/to/bin/activate # path/to => clone한 레포지토리 경로
$ pip install -r requirements.txt # venv 환경에서 학습에 필요한 pip 모듈 한 번에 설치
```
<br>

> start learning
<br>

```bash
$ python relative_word.py # w2v 모델 학습 
$ python relative_docs.py # d2v 모델 학습 
```
<br>


> close to venv 
<br>

```bash
$ deactivate
```
<br>

> cron script 
<br>


```bash 
$ 0 19 * * * /bin/bash -c 'source /home/recsys/bin/activate && python /home/recsys/src/relative_docs.py >> /home/recsys/cron.log 2>&1' # d2v   

$ 0 19 * * * /bin/bash -c 'source /home/recsys/bin/activate && python /home/recsys/src/relative_word.py >> /home/recsys/cron.log 2>&1' # w2v 
```

<br>

### colab 기준
<br>

* 별도로 가상화 시킬 필요없이 코드 + .env 파일에 환경변수만 잘 정의해주면 됨. 
* recsys-prac 부분에서 csv import 하는 부분만 제거하고 DB 연결 하는 부분만 변경하면 됨. 

<br>

```bash
#colab 용 konlpy 모듈
!curl -s https://raw.githubusercontent.com/teddylee777/machine-learning/master/99-Misc/01-Colab/mecab-colab.sh | bash

# 위 모듈 설치후 나머지 recsys-prac 코드 참고, csv -> db연결 후 파싱해주면 됨. 
```



