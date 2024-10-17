# from langchain.pydantic_v1 import BaseModel
from functools import lru_cache
from typing_extensions import TypedDict
from pydantic import BaseModel
from typing import List, Literal, Optional
from pydantic_settings import BaseSettings


class MilvusSettings(BaseSettings):
    milvus_host: str
    milvus_port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """

    question: str
    history: str
    generation: str
    documents: List[str]
    hallucinate_cnt: int
    retrieve_cnt: int


@lru_cache
def get_milvus_settings() -> MilvusSettings:
    return MilvusSettings()
