<h1 align="center">🕸️ SPIDER-RAG 🕸️</h1>

<p align="center"><img src="https://github.com/sigirace/spider/blob/main/images/main.png?raw=true" width="400" height="200"></p>

<p align="center">LangGraph를 사용한 멀티턴 RAG 어플리케이션</p>

## 📜 목차

- [프로젝트 개요](#🌈-프로젝트-개요)
- [기술 스택](#📚-기술-스택)

## 🌈 프로젝트 개요

<a href="http://spider-rag.duckdns.org/">
    <img src="https://github.com/sigirace/spider/blob/main/images/example.png?raw=true">
    <p>
        🔗 프로젝트 바로가기
    </p>
</a>

`Spider RAG`는 `LangGraph`를 활용하여 `RAG`를 구현한 챗봇 애플리케이션입니다. 이 앱은 보유한 문서 기반에서 관련 정보를 검색하고, 이를 생성 모델과 결합하여 더욱 정확하고 문맥에 맞는 응답을 제공합니다. 만약 보유한 문서로 답변을 할 수 없는 경우에는 `Web Search`를 통해 최신 정보를 검색하여 답변을 제공합니다. 또한 사용자의 대화를 기억하고 이를 기반으로 대화를 이어나가는 `멀티턴` 기능을 제공합니다. 이를통해 `Spider RAG`는 다양한 상황에서 보다 지능적이고 정보에 기반한 결과를 제공할 수 있습니다.

## 📚 기술 스택

<br>
<div align=center> 
<img src="https://img.shields.io/badge/nom-CB3837?style=flat&logo=npm&logoColor=white"/><img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=React&logoColor=white"/><img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=TypeScript&logoColor=white"/><img src="https://img.shields.io/badge/Chakraui-319795?style=flat&logo=Chakraui&logoColor=white"/>
<br>
<img src="https://img.shields.io/badge/Poetry-60A5FA?style=flat&logo=Poetry&logoColor=white"/><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/><img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white"/><img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=LangChain&logoColor=white"/><img src="https://img.shields.io/badge/celery-37814A?style=flat&logo=celery&logoColor=white"/><br>
<img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=MySQL&logoColor=white"/><img src="https://img.shields.io/badge/Milvus-00A1EA?style=flat&logo=Milvus&logoColor=white"/><img src="https://img.shields.io/badge/Redis-FF4438?style=flat&logo=Redis&logoColor=white"/><br>
<img src="https://img.shields.io/badge/Oracle-F80000?style=flat&logo=Oracle&logoColor=white"/><img src="https://img.shields.io/badge/NGINX-009639?style=flat&logo=NGINX&logoColor=white"/><img src="https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=Gunicorn&logoColor=white"/><img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=Docker&logoColor=white"/><br><br>

</div>

### 🖥️ Frontend

- `npm`: Frontend 라이브러리와 패키지 관리
- `React`: UI, 대화형 웹 애플리케이션 구축 라이브러리
- `Typescript`: 정적 타입 추가로 코드 안정서오가 유지보수성 향상
- `Chakra UI`: UI 컴포넌트 스타일

### 🚪 Backend

- `Poetry`: Python 의존성 관리 도구
- `Django`: API 서버로 주요 로직 담당
- `Python`: Backend 언어
- `Langchain`: LLM 사용을 위한 프레임워크
- `Celery`: 비동기 작업 큐

### 💾 Database

- `Milvus`: 문서 임베딩 저장 및 Retriever를 위한 Vector Database
- `Mysql`: 채팅기록 관리를 위한 RDB
- `Redis`: 비동기 작업 큐를 위한 브로커 수행

### 🚧 Server & Infra

- `Oracle Cloud Infrastructure`: Cloud 환경
- `Docker`: Container 기반 애플리케이션
- `Nginx`: Web server
- `Gunicorn`: Application Server

## 📐 시스템 아키텍처

<p align="center">
    <img src="https://github.com/sigirace/spider/blob/main/images/architecture.png?raw=true">
</p>

전체 시스템은 Oracle Cloud의 Instance에서 3가지 영역으로 크게 나뉘어 있습니다.
<br><br>
첫 번째로 `Code Area`입니다. Local에서 기능 구현을 위해 frontend/ backend 코드를 작성하고, github를 통해 코드를 pull 합니다.
<br><br>
두 번째는 `Dev Area`입니다. 이곳에서는 작성한 Code가 실제로 잘 동작하는지 테스트를 수행합니다. 웹 서버와 애플리케이션 서버는 사용하지 않으며 단순히 임시 서버를 구동하는 개발 모드로 실행됩니다. 이때 생성한 DB는 실제 서비스와 분리하여 구성합니다. 테스트는 기능 확인 및 각 서버간의 통신 여부를 확인합니다.
<br><br>
마지막으로 `Product Area`는 실제 서비스가 배포되는 공간입니다. 웹 서버와 애플리케이션 서버가 실행되며 모든 서버간의 통신이 이루어집니다. 이때 생성된 DB는 테스트 환경과 분리되어 실제 서비스를 위해 구성됩니다. 각 컨테이너마다 Nginx를 통해 클라이언트와 통신하며 요청을 처리합니다.

## 🔗 채팅 및 요약 프로세스

`채팅 프로세스`는 위 flowchart와 같이 구성하였습니다. 클라이언트로부터 채팅을 입력받으면 처음 채팅을 하는지 판단하고, 처음 채팅을 하는 경우 채팅방을 생성합니다. 채팅방이 생성되면 입력받은 메세지를 통해 OpenAI와 통신하며 답을 받고 그 내용을 채팅방에 저장합니다. 이후 채팅방에 이름이 있는지 확인하여 이름이 없다면 채팅방의 이름을 첫번째 대화를 사용하여 생성하고, 이름이 있다면 요약 요청을 보냅니다.

`요약 프로세스` 또한 위 flowchart와 같이 구성하였습니다. 클라이언트로부터 요약을 요청하면 현재 채팅방의 마지막 요약 Message ID를 조회합니다. 현재 채팅방의 마지막 요약 Message ID가 없다면 채팅방의 모든 대화를 요약하고, 있다면 마지막 요약 Message ID 이후 3턴(1턴은 Human-AI 쌍)이 지났는지 확인합니다. 3턴이 지났다면 과거 요약 메세지와 새로운 대화를 합쳐 새로운 요약 메세지를 생성합니다. 이는 불필요한 요약 생성을 방지하여 `요약 프로세스`의 `효율성`을 높이기 위함입니다. 요약된 채팅 메세지는 채팅 프로세스에서 LLM에게 함께 전달되어 `멀티턴` 기능을 수행합니다.

## 📍 실행 및 테스트

데이터 베이스/ 프론트엔드/ 백엔드

- 각 ReadMe 참조

## ❤️‍🔥 적용 사항

### 1. LangGraph

랭그래프 적용

- 무한루프 방지
- Agent, Tool 보다 나은 이유

### 2. 멀티턴

- 요약 메세지 생성 방식

### 3. 동시성

- celery 적용
- celery 내용

### 4. 임베딩 중복 방지

- 문서 해시값 저장

## ✏️ 향후 계획

- Multi Modal
- 비동기 펌프
