## AccountBook-Python Flask
- WAP 2017년도 겨울방학 프로젝트
- 파이썬 플라스크/MYSQL 등을 이용한 웹 장부시스템

## 개발목표
- MYSQL 및 Python flask를 이용한 웹서비스 구현
- 기본적인 알고리즘과 실력 향샹을 목표

## 미리보기
- ppt 디렉토리의 pdf 파일을 참고하시기 바랍니다.

![1](https://user-images.githubusercontent.com/28443896/36150603-9369bd98-1107-11e8-8154-4688a0603ff7.png)

![2](https://user-images.githubusercontent.com/28443896/36150610-97614182-1107-11e8-9620-e8a818987869.png)

![4](https://user-images.githubusercontent.com/28443896/36150615-9b268606-1107-11e8-810a-b337ed79b2ea.png)

![3](https://user-images.githubusercontent.com/28443896/36150618-9b6e86b8-1107-11e8-9611-ec73e6254214.png)

![5](https://user-images.githubusercontent.com/28443896/36150619-9b996de2-1107-11e8-9148-2380a9bd49d1.png)


## 웹 전자장부 사용법 (web_server.py)
- mysql version : 5.6
- python version : 3.6

#### 1. 소스코드 다운로드
`git clone https://github.com/etilelab/AccountBook-Flask.git`


#### 2. SQL파일 실행
```
mysql: source ~/db/create_db.sql
mysql: source ~/db/create_table.sql
mysql: source ~/db/create_all_sp.sql.sql
```
#### 3. setObject.py 설정
기본적인 설정을 해준다.
```
db_user = "root"
db_password = "password"
db_host = "localhost"
db_name = "accountBook"

recaptcha_site_key ="google recaptcha site key"
recaptcha_secret_key = "google recaptcha secret key"
```

## 프로젝트 일정
트렐로 사용


## 활용 기술
- MYSQL
- Python Flask
- Bootstrap
- AWS EC2 ubuntu
