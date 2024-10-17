from typing import List
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from schemas.structured_model import (
    GradeDocuments,
    GradeHallucinations,
    RouteQuery,
    WebRouteQuery,
)
from langchain_core.documents import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from llms.vectordb.vectorstore import VectorDB


class ChainModules:
    def __init__(
        self,
        llm: ChatOpenAI,
        max_web_results: int = 3,
    ):
        self.max_web_results = max_web_results
        self.llm = llm

    def summary(self, summary: str, new_line: str) -> str:
        """
        langchain.memory.ConversationSummaryBufferMemory의 요약 모듈
        """
        summary_system_msg = """제공된 대화 내용을 점진적으로 요약하고 이전 요약에 새로운 요약을 추가합니다.\n
        예시\n
        현재 요약:\n
        인간은 인공지능에 대해 인공지능이 어떻게 생각하는지 묻습니다. 인공지능은 인공지능이 선을 위한 힘이라고 생각합니다.\n
        새로운 대화 라인:\n
        인간: 인공 지능이 선을 위한 힘이라고 생각하는 이유는 무엇인가요?\n
        AI: 인공 지능은 인간이 잠재력을 최대한 발휘하는 데 도움이 될 것이기 때문입니다.\n
        새 요약:\n
        인간은 인공 지능에 대해 인공 지능이 어떻게 생각하는지 묻습니다. 인공 지능은 인간이 잠재력을 최대한 발휘하는 데 도움이 될 것이기 때문에 인공 지능은 선을 위한 힘이라고 생각합니다.\n
        예제 끝\n\n
        """

        summary_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", summary_system_msg),
                (
                    "human",
                    "현재 요약:\n{summary}\n새로운 대화 라인:\n{new_line}\n새 요약:",
                ),
            ]
        )

        summary_chain = summary_prompt | self.llm | StrOutputParser()

        return summary_chain.invoke({"summary": summary, "new_line": new_line})

    def naming(self, history: str) -> str:

        naming_system_msg = """당신은 주어진 대화 기록을 바탕으로 채팅방 이름을 생성하는 전문가입니다.\n인간과 AI의 대화 기록을 바탕으로 채팅방 이름을 생성하여 주세요.\n채팅방 이름은 인간의 질문에 초점을 맞춰야 합니다.\n명사구를 나열하는 방식으로 간략하며 이해하기 쉽게 생성하세요.\n채팅방 이름 전체에 따옴표를 적용하는 것은 불허합니다."""

        naming_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", naming_system_msg),
                ("human", "{history}"),
            ]
        )

        naming_chain = naming_prompt | self.llm | StrOutputParser()

        return naming_chain.invoke({"history": history})

    def common(self, history: str, question: str) -> str:

        print("*****[Module]common*****")

        common_system_msg = """당신은 질문에 대한 답변을 주는 챗봇 SPIDER입니다."""

        common_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", common_system_msg),
                ("human", "{history} \n\n 사용자의 질문: \n\n {question}"),
            ]
        )

        common_chain = common_prompt | self.llm | StrOutputParser()

        return common_chain.invoke({"history": history, "question": question})

    def router(self, history: str, question: str) -> RouteQuery:

        print("*****[Module]router*****")

        router_system_msg = """당신은 사용자 질문을 vectorstore, common으로 라우팅하는 전문가입니다.\n'사용자의 질문이 금융, 마이데이터와 관련되어있거나 표준 API 규격과 같은 정보통신 기술에 관한 질문일 경우 vectorstore으로 대답합니다.\n그외 아주 일반적인 대화에 대해서만 common으로 대답합니다.\n사용자 질문을 우선으로 평가하며 필요한 경우에 과거 대화 기록을 참조하세요."""

        router_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", router_system_msg),
                ("human", f"{history}\n\n사용자 질문: {question}"),
            ]
        )

        router_chain = router_prompt | self.llm.with_structured_output(RouteQuery)

        return router_chain.invoke({"history": history, "question": question})

    def web_router(self, history: str, question: str) -> WebRouteQuery:

        print("*****[Module]web_router*****")

        web_router_system_msg = """당신은 사용자 질문을 common, web_search로 라우팅하는 전문가입니다.\n언어모델이 사용자와의 과거 대화 혹은 이미 알고 있는 지식에 대해서는 common으로 대답합니다.\n새로운 지식을 필요로 하는 질문에 대해서는 web_search로 대답합니다.\n사용자 질문을 우선으로 평가하며 필요한 경우에 과거 대화 기록을 참조하세요."""

        web_router_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", web_router_system_msg),
                ("human", f"{history}\n\n사용자 질문: {question}"),
            ]
        )

        web_router_chain = web_router_prompt | self.llm.with_structured_output(
            WebRouteQuery
        )

        return web_router_chain.invoke({"history": history, "question": question})

    def retrieval_grader(self, document: str, question: str) -> GradeDocuments:

        print("*****[Module]retrieval_grader*****")

        retrieval_grader_system_msg = """당신은 검색된 문서와 사용자 질문의 관련성을 평가하는 채점자입니다.\n문서에 사용자 질문과 관련된 키워드 또는 의미론적 의미가 포함된 경우 관련성이 있는 것으로 등급을 매깁니다.\n엄격한 테스트일 필요는 없습니다. 목표는 잘못된 검색을 걸러내는 것입니다.\n'yes' 또는 'no'를 사용하여 문서와 질문의 관련성을 평가합니다."""

        retrieval_grader_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", retrieval_grader_system_msg),
                ("human", "검색된 문서: \n\n {document} \n\n 사용자 질문: {question}"),
            ]
        )

        retrieval_grader_chain = (
            retrieval_grader_prompt | self.llm.with_structured_output(GradeDocuments)
        )

        return retrieval_grader_chain.invoke(
            {"document": document, "question": question}
        )

    def rag(self, history: str, documents: List[Document], question: str) -> str:

        print("*****[Module]rag*****")

        rag_system_msg = """당신은 주어진 질문에 대한 답변을 하는 전문가입니다.\n다음 검색된 문서를 사용하여 질문에 답하세요.\n답을 모르면 모른다고 말하세요.\n필요할 경우에만 과거 대화 기록을 참조하세요.\n답변은 최대한 상세하게 작성되어야 합니다.\n마지막에 참조한 문서의 이름과 페이지를 언급하세요."""

        rag_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", rag_system_msg),
                (
                    "human",
                    "{history} \n\n 검색된 문서: \n\n {documents} \n\n 사용자 질문: {question}",
                ),
            ]
        )

        rag_chain = rag_prompt | self.llm | StrOutputParser()

        return rag_chain.invoke(
            {"history": history, "documents": documents, "question": question}
        )

    def web_rag(self, history: str, documents: List[Document], question: str) -> str:

        print("*****[Module]web_rag*****")

        web_rag_system_msg = """당신은 주어진 질문에 대한 답변을 하는 전문가입니다.\n제시된 문서는 웹 검색을 통해 얻은 문서입니다.\n이를 사용하여 질문에 답하세요.\n답변은 최대한 상세하게 작성되어야 합니다.\n답을 모르면 모른다고 말하세요.\n필요할 경우에만 과거 대화 기록을 참조하세요.\n마지막에 참조한 웹 사이트의 정보를 언급하고 링크를 제시하세요."""

        web_rag_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", web_rag_system_msg),
                (
                    "human",
                    "{history} \n\n 검색된 문서: \n\n {documents} \n\n 사용자 질문: {question}",
                ),
            ]
        )

        rag_chain = web_rag_prompt | self.llm | StrOutputParser()

        return rag_chain.invoke(
            {"history": history, "documents": documents, "question": question}
        )

    def hallucination_grader(
        self,
        history: str,
        documents: List[Document],
        generation: str,
    ) -> GradeHallucinations:

        print("*****[Module]hallucination_grader*****")

        hallucination_system_msg = """검색된 문서를 사실이라고 보고, 사실에 근거하여 답변을 생성하고있는지 여부를 평가하는 등급입니다.\n'yes', 'no'를 사용하여 평가합니다.\n'yes'는 답이 사실에 근거하는 것을 의미합니다.\n'no'는 답변이 문서에 기반하지 않음을 의미합니다.\n 단, 너무 엄격할 필요는 없기에 문서와 답변의 의미가 일치하면 'yes'로 평가합니다.\n필요할 경우에만 과거 대화 이력을 참조하세요."""

        hallucination_grader_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", hallucination_system_msg),
                (
                    "human",
                    "{history}\n\n 검색된 문서(사실): \n\n {documents} \n\n LLM의 답변: {generation}",
                ),
            ]
        )

        hallucination_grader_chain = (
            hallucination_grader_prompt
            | self.llm.with_structured_output(GradeHallucinations)
        )

        return hallucination_grader_chain.invoke(
            {
                "history": history,
                "documents": documents,
                "generation": generation,
            }
        )

    def re_write(self, history: str, question: str) -> str:

        print("*****[Module]re_write*****")

        re_write_system_msg = """당신은 입력 질문을 금융 마이데이터 관점에서 최적화하여 변환하는 질문 재작성자입니다.\n사용자의 질문의 의도/의미를 추론해 보세요.\n최종 출력은 원래 질문과 동일한 의미를 가지면서 금융 마이데이터의 관점에서 더 나은 질문을 생성해야 합니다.\n필요할 경우에만 과거 대화 이력을 참조하세요."""

        re_write_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", re_write_system_msg),
                (
                    "human",
                    "{history} \n\n 사용자의 초기 질문: \n\n {question}\n개선된 질문:",
                ),
            ]
        )

        re_write_chain = re_write_prompt | self.llm | StrOutputParser()

        return re_write_chain.invoke({"history": history, "question": question})

    def re_write_for_web(self, history: str, question: str) -> str:

        print("*****[Module]re_write_for_web*****")

        re_write_for_web_system_msg = """당신은 입력 질문을 금융 마이데이터에 대한 내용을 포함하고, 웹 검색에 맞게 최적화하여 변환하는 질문 재작성자입니다.\n금융 마이데이터에 대한 내용을 더해 질문을 개선하세요.\n웹 검색을 위한 질문은 반드시 명사구로만 작성되어야 합니다.\n아래 예시를 참조하세요.\n[예시]\n1. 사용자의 초기 질문: 포켓몬고 어떻게 설치해? -> 개선된 질문: 포켓몬고 설치 방법\n2. 사용자의 초기 질문: 흑백요리사에서 가장 인기있는 요리는 무엇인가요?-> 개선된 질문: 흑백 요리사 인기 요리\n\n필요할 경우에만 과거 대화 이력을 참조하세요."""

        re_write_for_web_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", re_write_for_web_system_msg),
                (
                    "human",
                    "{history} \n\n 사용자의 초기 질문: \n\n {question}\n개선된 질문:",
                ),
            ]
        )

        re_write_for_web_chain = re_write_for_web_prompt | self.llm | StrOutputParser()

        return re_write_for_web_chain.invoke({"history": history, "question": question})

    def web_search_tool(self) -> TavilySearchResults:
        return TavilySearchResults(max_results=self.max_web_results)
