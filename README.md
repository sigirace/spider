<h1 align="center">🕸️ SPIDER-RAG 🕸️</h1>

<p align="center"><img src="https://github.com/sigirace/spider/blob/main/images/main.png?raw=true" width="400" height="200"></p>

<p align="center">LangGraph를 사용한 멀티턴 RAG 어플리케이션</p>

## 📜 목차

- [프로젝트 개요](#🌈-프로젝트-개요)
- [기술 스택](#📚-기술-스택)
- [시스템 아키텍처](#📐-시스템-아키텍처)
- [채팅 및 요약 프로세스](#🔗-채팅-및-요약-프로세스)
- [실행 및 테스트](#📍-실행-및-테스트)
- [개발 적용 사항](#❤️‍🔥-개발-적용-사항)
- [향후 계획](#✏️-향후-계획)

## 🌈 프로젝트 개요

<a href="http://spider-rag.duckdns.org/">
  <img src="https://github.com/sigirace/spider/blob/main/images/example.png?raw=true">
  🔗 프로젝트 바로가기  
</a>

<br>

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
- `React`: 대화형 웹 애플리케이션 구축 라이브러리
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
    <p align="center">&lt;시스템 아키텍처&gt;</p>
</p>

전체 시스템은 Oracle Cloud의 Instance에서 3가지 영역으로 크게 나뉘어 있습니다.
<br>

첫 번째로 `Code Area`입니다. Local에서 기능 구현을 위해 frontend/ backend 코드를 작성하고, github를 통해 코드를 pull 합니다.
<br>

두 번째는 `Dev Area`입니다. 이곳에서는 작성한 Code가 실제로 잘 동작하는지 테스트를 수행합니다. 웹 서버와 애플리케이션 서버는 사용하지 않으며 단순히 임시 서버를 구동하는 개발 모드로 실행됩니다. 이때 생성한 DB는 실제 서비스와 분리하여 구성합니다. 테스트는 기능 확인 및 각 서버간의 통신 여부를 확인합니다.
<br>

마지막으로 `Product Area`는 실제 서비스가 배포되는 공간입니다. 웹 서버와 애플리케이션 서버가 실행되며 모든 서버간의 통신이 이루어집니다. 이때 생성된 DB는 테스트 환경과 분리되어 실제 서비스를 위해 구성됩니다. 각 컨테이너마다 Nginx를 통해 클라이언트와 통신하며 요청을 처리합니다.

## 🔗 채팅 및 요약 프로세스

<details>
<summary>채팅 프로세스</summary>
<p align="center">
<img src="https://github.com/sigirace/spider/blob/main/images/chat_process.png?raw=true" width="350" height="500">
</p>
</details>
<br>

`채팅 프로세스`는 위 flowchart와 같이 구성하였습니다. 클라이언트로부터 채팅을 입력받으면 처음 채팅을 하는지 판단하고, 처음 채팅을 하는 경우 채팅방을 생성합니다. 채팅방이 생성되면 입력받은 메세지를 통해 OpenAI와 통신하며 답을 받고 그 내용을 채팅방에 저장합니다. 이후 채팅방에 이름이 있는지 확인하여 이름이 없다면 채팅방의 이름을 첫번째 대화를 사용하여 생성하고, 이름이 있다면 요약 요청을 보냅니다.<br>

<details>
<summary>채팅 요약 프로세스</summary>
<p align="center">
<img src="https://github.com/sigirace/spider/blob/main/images/summary_process.png?raw=true" width="300" height="400">
</p>
</details>

<br>

`요약 프로세스` 또한 위 flowchart와 같이 구성하였습니다. 클라이언트로부터 요약을 요청하면 현재 채팅방의 마지막 요약 Message ID를 조회합니다. 현재 채팅방의 마지막 요약 Message ID가 없다면 채팅방의 모든 대화를 요약하고, 있다면 마지막 요약 Message ID 이후 3턴(1턴은 Human-AI 쌍)이 지났는지 확인합니다. 3턴이 지났다면 과거 요약 메세지와 새로운 대화를 합쳐 새로운 요약 메세지를 생성합니다. 이는 불필요한 요약 생성을 방지하여 `요약 프로세스`의 `효율성`을 높이기 위함입니다. 요약된 채팅 메세지는 채팅 프로세스에서 LLM에게 함께 전달되어 `멀티턴` 기능을 수행합니다.

## 📍 실행 및 테스트

### 1. 실행

전체 프로젝트는 `DB 영역` 기동 후 `Application 영역`을 기동해야 합니다. 각 영역의 기동을 위해서 `docker-compose`를 사용합니다.

**1.1 Databases 환경설정**

```
# databases > docker-compose.yml

# MySQL 데이터베이스
mysql:
  image: mysql:latest
  container_name: mysql
  environment:
    MYSQL_ROOT_PASSWORD: your_password
    TZ: Asia/Seoul
  ports:
    - "3306:3306"
  volumes:
    - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/mysql:/var/lib/mysql
```

- `MYSQL_ROOT_PASSWORD`: docker container로 실행할 Mysql DB password를 설정합니다.

```
> cd databases
> docker-compose up -d
```

**1.2 Backend**

```
# docker-compose.yml

spider-backend:
  build: ./spider-backend
  container_name: spider-backend
  environment:
    - HOST=your_domain_or_ip
    - DB_NAME=spider
    - DB_USER=your_db_user
    - DB_PASSWORD=your_db_password
    - DB_PORT=your_db_port
    - DB_HOST=your_db_host
    - MILVUS_PORT=your_milvus_port
    - MILVUS_HOST=your_milvus_host
    - OPENAI_API_KEY=your_openai_api_key
    - TAVILY_API_KEY=your_tavily_api_key
    - REDIS_PORT=your_redis_port
    - REDIS_HOST=your_redis_host
  ports:
    - "8000:8000"
```

- `Backend`에서 바라볼 `DB 영역`의 정보들을 입력합니다.

```
> docker-compose up -d --build
```

### 2. 테스트

개별 서버 기동 및 테스트는 각 영역별 README 파일을 참조해 주세요.

- [Backend](https://github.com/sigirace/spider/blob/main/spider-backend/README.md)
- [Frontend](https://github.com/sigirace/spider/blob/main/spider-frontend/README.md)

## ❤️‍🔥 개발 적용 사항

### 1. LangGraph

**1.1 LangGraph 사용 이유**

RAG 기반 챗봇을 구성하기 위해 `LangGraph` 아키텍처를 사용하였습니다. 기존의 에이전트나 Tool/Function Calling 아키텍처는 LLM의 의사 결정을 추적하고 제어하기 복잡하다는 단점이 있어, 간단한 질문에도 LLM의 결과를 예측하기 어려운 경우가 많았습니다. 따라서 결과 예측이 쉽고 사용자에게 일관적인 답변을 줄 수 있게 아래와 같은 흐름으로 `LangGraph`를 구성하였습니다.

<p align="center">
    <img src="https://github.com/sigirace/spider/blob/main/images/langgraph.png?raw=true"
    height="500">
</p>
<p align="center"> &lt;RAG를 위한 LangGraph 아키텍처 설계&gt; </p>

<br>

<details>
<summary>LangGraph 장점</summary>
<br>

1. **명시적이고 직관적인 워크플로우**: LangGraph는 작업 흐름을 그래프 형태로 명시적으로 정의할 수 있어, 복잡한 논리적 흐름이나 여러 단계를 시각적으로 표현하고 관리하기가 쉽습니다. 이로 인해 여러 도구를 조합하고 작업을 분기하거나 순차적으로 처리할 때, 흐름을 명확하게 이해하고 제어할 수 있습니다.

2. **효율적인 실행 계획**: Agent와 Tool Calling 방식은 보통 각 단계에서 필요한 도구를 호출하며 유연성을 제공하지만, 그만큼 불필요한 중간 호출이나 대기 시간이 발생할 수 있습니다. LangGraph는 전체 실행 계획을 미리 정의하여 불필요한 호출을 줄이고, 각 단계가 어떻게 연결되고 실행될지를 최적화할 수 있어 더 효율적입니다.

3. **유지보수성과 확장성**: LangGraph는 그래프 기반 설계 덕분에 새로운 도구나 작업 단계를 추가하는 것이 상대적으로 간단하며, 코드가 커지더라도 이를 체계적으로 관리하고 확장할 수 있는 구조를 제공합니다. 반면, Agent나 Tool Calling은 규칙 기반 로직이나 조건이 복잡해질수록 관리가 어려워질 수 있습니다.

4. **의존성 관리와 오류 처리**: LangGraph에서는 각 단계 간의 의존성을 명확하게 설정할 수 있어, 어떤 도구가 언제 실행되어야 하는지, 실패했을 때 어떤 대응이 필요한지를 명확히 정의할 수 있습니다. Agent 방식은 이런 의존성 관리를 암묵적으로 수행하는 경우가 많아, 예상치 못한 오류 처리나 흐름 제어가 복잡해질 수 있습니다.

5. **일관성과 신뢰성**: LangGraph는 의사 결정 분기를 명확하게 정의하여, 답변의 검증이나 더 나은 결정을 위한 단계를 체계적으로 수립할 수 있습니다. 이를 통해 할루시네이션, 잘못된 질의 등의 문제를 해결하여 LLM의 출력을 더욱 신뢰할 수 있게 만듭니다.
</details>

<br>

**1.2 LangGraph 단점 및 개선 사항**

`LangGraph`를 사용하여 의사결정의 각 분기가 명확해짐에 따라 질문의 개선, 문서 및 할루시네이션 검증의 단계를 수립하였습니다. 하지만 테스트를 수행하며 Router 단계에서 RAG 수행에 대한 의사결정이 잘못되었을 때, 그래프가 가지는 연결성 때문에 무한 루프에 빠지는 경우가 발생하였습니다.

```
[무한루프 예시]
질의: 문서 지식에 포함되어있지 않으나 유사 도메인의 질문
라우터: 유사 도메인이기에 RAG로 라우팅
문서평가/거짓평가: 질문을 해결할 수 있는 문서 혹은 답변이 나오지 않기에 재평가 수행
```

이를 해결하기 위해 의사결정의 주요 분기에서 루프에 대한 조건을 체크하는 규칙을 추가하여 일정 수행 내에 답변을 얻지 못할시 Web 검색으로 새로운 문서를 찾아 답변할 수 있게 라우팅하였습니다. 또한, 각 단계에서의 의사결정을 더 정교하게 다듬기 위해 프롬프트를 개선하는 과정을 거쳤습니다. 이러한 과정은 사용자가 언제나 믿을 수 있는 답변을 제공받을 수 있도록 시스템의 일관성과 안정성을 강화했습니다.

### 2. 프롬프트 엔지니어링

`Few-shot`을 통한 프롬프트 구성으로 LLM 수행 결과의 품질과 일관성을 향상시켰습니다.

**2.1 멀티턴을 위한 대화 요약**

앞서 [채팅 및 요약 프로세스](#🔗-채팅-및-요약-프로세스)를 통해 채팅을 요약하여 멀티턴을 수행하는 방법을 설명하였습니다. 이때 요약은 Langchain의`ConversationSummaryBufferMemory` 방식을 참조하여 수행하였습니다. Langchain 라이브러리에서 제공하는 다양한 메모리 유형 중 이를 선택한 이유는 요약의 크기를 효율적으로 관리할 수 있기 때문입니다. 해당 클래스에서는 `BasePromptTemplate`의 `SUMMARY_PROMPT`를 사용하고 있기에 이를 한국어로 번역하여 아래와 같은 프롬프트를 구성하였습니다.

```
system: 제공된 대화 내용을 점진적으로 요약하고 이전 요약에 새로운 요약을 추가합니다.
[예시]
- 현재 요약: 인간은 인공지능에 대해 인공지능이 어떻게 생각하는지 묻습니다. 인공지능은 인공지능이 선을 위한 힘이라고 생각합니다.
- 새로운 대화 라인:
	- 인간: 인공 지능이 선을 위한 힘이라고 생각하는 이유는 무엇인가요?\n
	- AI: 인공 지능은 인간이 잠재력을 최대한 발휘하는 데 도움이 될 것이기 때문입니다.\n
- 새 요약: 인간은 인공 지능에 대해 인공 지능이 어떻게 생각하는지 묻습니다. 인공 지능은 인간이 잠재력을 최대한 발휘하는 데 도움이 될 것이기 때문에 인공 지능은 선을 위한 힘이라고 생각합니다.
[예제 끝]
human: 현재 요약: {summary} 새로운 대화 라인:{new_line} 새 요약:
```

**2.2 웹 검색을 위한 질의 재구성**

구성된 LangGraph 아키텍처에서는 일관되고 신뢰성 있는 답변을 제공하기 위해 Web 검색으로의 분기를 설정하였습니다. 하지만 챗봇에게 하는 질문과 일반 웹 검색에 사용되는 질문은 성격이 다릅니다. 따라서 웹 검색시 검색의 질을 높이기 위해서는 사용자의 질문을 일반적인 검색 엔진에 적합한 형태로 재구성하는 과정을 아래와 같은 프롬프트로 도입하였습니다.

```
system: 당신은 입력 질문을 웹 검색에 맞게 최적화하여 변환하는 질문 재작성자입니다. 사용자의 의도를 파악하여 질문을 개선하세요. 웹 검색을 위한 질문은 반드시 명사구로만 작성되어야 합니다.아래 예시를 참조하세요.
[예시]
- 사용자의 초기 질문: 포켓몬고 어떻게 설치해?
- 개선된 질문: 포켓몬고 설치 방법
- 사용자의 초기 질문: 흑백요리사에서 가장 인기있는 요리는 무엇인가요?
- 개선된 질문: 흑백 요리사 인기 요리
[예제 끝]
human: 사용자의 초기 질문: {question} 개선된 질문:
```

### 3. 동시성 처리

**3.1 Celery 아키텍처**

<p align="center">
    <img src="https://github.com/sigirace/spider/blob/main/images/celery_architecture.png?raw=true" width="400" height="200">
    <p align="center">&lt;Celery 아키텍처&gt;</p>
</p>

구성한 시스템에서 백엔드는 Django를 사용하고 애플리케이션 서버는 Gunicorn으로 설정하였습니다. Gunicorn은 3개의 워커를 띄워 요청을 처리하도록 구성되었지만, API 수행 시간이 오래걸린다면 서버 프로세스가 점유되어 최대 3명의 유저만이 서비스를 이용할 수 있는 단점이 있습니다. 특히 LangGraph는 하나의 질의에 여러번의 LLM API가 수행되기 때문에 동시성 처리에 대한 해결이 필요합니다. 이를 해결하기 위해 LangGraph의 수행을 비동기적으로 처리할 수 있도록 async Celery task로 변경하였습니다.

**3.2 Celery 수행 프로세스**

<p align="center">
    <img src="https://github.com/sigirace/spider/blob/main/images/celery_process.png?raw=true" width="400" height="250">
    <p align="center">&lt;Celery 수행 프로세스&gt;</p>
</p>

프로세스는 구성된 시스템에서 클라이언트의 요청을 백엔드의 Django가 Message Broker에게 전달합니다. 이후 클라이언트는 응답에 대한 지속적인 요청을 보내게 되고 django가 이를 받아 task의 수행을 조회하며 결과와 함께 클라이언트에 전달하게 됩니다.

### 4. 임베딩 중복 방지

새로운 문서가 입력될 때 기존 문서와 비교하여 `중복`을 방지하는 임베딩 모듈을 설계했습니다. 아래는 Milvus의 collection 스키마 입니다.

```
page_content,
metadata={
    "doc_name",
    "page_number",
    "creation_time",
    "modification_time",
    "key" #f"{file_name}_{page_number}_{hash_key}",
}
```

이때 metadata의 hash key는 page_content를 sha256방식으로 변한환 hash 값입니다. 이를 통해 임베딩 전 컬렉션에 해당하는 key 값이 있는지 조회하고 있다면 같은 문서로 판단하여 `중복`된 내용을 추가적으로 임베딩 하지 않도록 방지합니다. <br>

단, 현재는 문서를 임포트하는 전용 화면이 없지만, 이후 추가적인 문서를 활용할 때 효율성을 높일 수 있을 것입니다.

## ✏️ 향후 계획

- Multi Modal
- 비동기 펌프
