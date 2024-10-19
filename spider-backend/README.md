<h1 align="center">🚪 SPIDER-RAG Backend 🚪</h1>

## 📜 목차

- [개요](#📌-개요)
- [프로젝트 구조](#📌-프로젝트-구조)
- [DB 모델링](#📌-DB-모델링)
- [API 목록](#📌-API-목록)
- [실행방법](#📌-실행방법)
- [테스트](#📌-테스트)

## 📌 개요

### 1. 상세

`Backend` 구성은 python 기반의 django framework을 사용했으며 llm 인터페이스를 위해 langchain framework를 사용하였습니다. Langchain 래퍼는 대화형 애플리케이션을 구축하기 위해 `ChatOpenAI`를 사용하였고, `Document Embedding`을 위해서는 `OpenAIEmbeddings`를 통해 문서를 임베딩화 시켰습니다.

### 2. 주요 버전 정보

- `python`: 3.11.3
- `django`: 5.1.2
- `langchain`: 0.3.3
- `llm model`: ChatOpenAI(model="gpt-4o-mini", temperature=0)
- `embedding model`: OpenAIEmbeddings

## 📌 프로젝트 구조

```
├── chats
├── common
├── config
├── llms
│   ├── graphs
│   ├── vectordb
├── users
└── schemas
```

- `config`: django 설정
- `common`: 생성일 수정일 등 공통 모델 정의
- `chats`: 사용자와 대화를 위한 모델 및 API 설계, 생성된 LLM 래퍼를 통해 openAI와 통신
- `llms`: Langchain 래퍼 정의
  - `graphs`: LangGraph 아키텍처 정의
  - `vectordb`: Milvus 연동 및 embedding
- `users`: 미구현 (현재 유저별 독립된 테넌트로 관리하지 않고 모든 유저가 동일한 환경에서 사용하고 있습니다. )
- `schemas`: 모델 및 LangGraph 응답 정의

## 📌 DB 모델링

| Type              | Links                                                                                                                                                                                                                            |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 💾 **ER-Diagram** | [draw.io](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=spider.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1Qu3CR8UhbqCZ4PdBMRE3LbZZSVYkUY-9%26export%3Ddownload) |

## 📌 API 목록

| 주제        | 기능             | METHOD | API Path                   | Body        | Response                                                                                                        |
| ----------- | ---------------- | ------ | -------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------- |
| 채팅방      | 전체 채팅방 조회 | GET    | chat/room                  |             | [LIST][OBJECT]<br>chat_room_id: int<br>chat_room_name: str<br>chat_summary: str<br>created_at: str              |
| 채팅방 상세 | 채팅방 조회      | GET    | chat/room/chat_room_id     |             | [OBJECT]<br>chat_room_id: int<br>chat_room_name: str<br>chat_summary: str<br>created_at: str<br>updated_at: str |
|             | 채팅방 생성      | POST   | chat/room/chat_room_id     |             |                                                                                                                 |
|             | 채팅방 수정      | PUT    | chat/room/chat_room_id     | task:str    |                                                                                                                 |
|             | 채팅방 삭제      | DELETE | chat/room/chat_room_id     |             |                                                                                                                 |
| 메세지      | 메세지 조회      | GET    | chat/messages/chat_room_id |             | [LIST][OBJECT]<br>message_id: int<br>role: str<br>content: str<br>sender_id: str<br>created_at:str              |
|             | 메세지 생성      | POST   | chat/messages/chat_room_id | content:str |                                                                                                                 |
| 상태        | 상태 조회        | GET    | chat/status/task_id        |             | [OBJECT]<br>status: str                                                                                         |

## 📌 실행 방법

[전체 프로젝트 README](https://github.com/sigirace/spider?tab=readme-ov-file)의 시스템 아키텍처에서 설명하였듯, 애플리케이션 서버는 사용하지 않으며 단순히 임시 서버를 구동하는 개발 모드로 실행합니다.

### 1. Env

```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
MILVUS_HOST=your_milvus_host
MILVUS_PORT=your_milvus_posrt
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
REDIS_HOST=your_redis_host
REDIS_PORT=your_redis_port
```

- 프로젝트 폴더안에 `.env` 파일을 생성합니다.

### 2. Dependency

```
cd spider-backend
poetry shell
poetry install
```

### 3. DB migrate

```
python manage.py makemigration
python manage.py migrate
```

### 4. Runserver

```
python manage.py createsuperuser # 선택
python manage.py runserver
```

## 📌 테스트

### 1. Model

```
python manage.py test chats.test.test_chatroom_model.py
python manage.py test chats.test.test_chatmessages_model.py
```

### 2. API

```
python manage.py test chats.test.test_chatroom_view.py
python manage.py test chats.test.test_chatroom_detail_view.py
python manage.py test chats.test.test_chatmessages_view.py
```

### 3. Vector DB

```
python manage.py test llms.tests.tests_vectordb.py
```

### 4. Embedding

- 📒[문서 임베딩](https://github.com/sigirace/spider/blob/main/spider-backend/llms/vectordb/embedding.ipynb)

### 5. LangGraph

- 📒[단일 노드 및 엣지 테스트](https://github.com/sigirace/spider/blob/main/spider-backend/llms/graphs/unit_test.ipynb)
- 📒[통합 테스트](https://github.com/sigirace/spider/blob/main/spider-backend/llms/graphs/test.ipynb)
