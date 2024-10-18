# React 빌드를 위한 단계
FROM node:22 AS build

# 앱 디렉토리 설정
WORKDIR /app

# package.json과 package-lock.json 복사
COPY package*.json ./

# 의존성 설치
RUN npm install

# 소스 코드 복사 및 빌드
COPY . .
RUN npm run build

# Nginx를 위한 단계
FROM nginx:alpine

# 빌드된 React 앱 복사
COPY --from=build /app/build /usr/share/nginx/html

# Nginx 설정 복사
COPY ./nginx-frontend.conf /etc/nginx/conf.d/default.conf

# Nginx 포트 오픈
EXPOSE 80

# Nginx 실행
CMD ["nginx", "-g", "daemon off;"]