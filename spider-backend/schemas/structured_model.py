from typing import Literal
from pydantic import BaseModel, Field


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "common"] = Field(
        ...,
        description="사용자 질문이 주어지면 'vectorstore' 또는 'common'으로 라우팅하도록 선택합니다.",
    )


class WebRouteQuery(BaseModel):
    """WebRouteQuery a user query to the most relevant datasource."""

    datasource: Literal["common", "web_search"] = Field(
        ...,
        description="사용자 질문이 주어지면 'common' 또는 'web_search'으로 라우팅하도록 선택합니다.",
    )


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: Literal["yes", "no"] = Field(
        description="문서가 질문과 관련이 있는지 판단하여 'yes' 또는 'no'로 대답합니다."
    )


class GradeHallucinations(BaseModel):
    """Multiple score for hallucination present in generation answer."""

    multiple_score: Literal["yes", "no", "infinite"] = Field(
        description="생성된 답변이 사실에 기반하여 생성되었는지 판단하여 'yes' 또는 'no'로 대답합니다. 무한루프일 경우 'infinite'로 대답합니다."
    )


class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""

    binary_score: Literal["yes", "no"] = Field(
        description="생성된 답변이 질문에 대해 도움이 되는 답변인지 판단하여 'yes' 또는 'no'로 대답합니다."
    )
