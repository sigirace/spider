# Django 및 Gunicorn을 위한 기본 이미지
FROM python:3.11 AS build

# 작업 디렉토리 설정
WORKDIR /app

# poetry.lock과 pyproject.toml 파일 복사
COPY poetry.lock pyproject.toml ./

# 종속성 설치
RUN pip install poetry && poetry install --no-dev

# 소스 코드 복사
COPY . .

# start.sh 스크립트 복사 및 실행 권한 부여
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Nginx 설치
RUN apt-get update && apt-get install -y nginx

# Nginx 설정 파일 복사
COPY nginx-backend.conf /etc/nginx/conf.d/default.conf

# Nginx와 Gunicorn이 8000번 포트에서 동작하도록 설정
EXPOSE 8000

# Nginx와 Gunicorn 모두 실행
CMD ["/start.sh"]