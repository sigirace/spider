from django.apps import AppConfig
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from llms.graphs.edges import Edges
from llms.graphs.nodes import Nodes
from llms.modules import ChainModules
from llms.vectordb.vectorstore import VectorDB
from schemas.models import get_milvus_settings
from llms.graphs.builder import LangGraph


class LlmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "llms"

    def ready(self):
        global spider, chain

        chain = ChainModules(
            llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        )

        vector_db = VectorDB(
            settings=get_milvus_settings(),
            embedding=OpenAIEmbeddings(),
        )

        nodes = Nodes(
            vector_db=vector_db,
            chain_modules=chain,
            collection_name="document_embeddings",
        )

        edges = Edges(chain_modules=chain)

        spider = LangGraph(nodes=nodes, edges=edges)
