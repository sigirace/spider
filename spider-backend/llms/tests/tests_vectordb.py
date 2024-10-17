from django.test import TestCase
from unittest.mock import patch, MagicMock
from llms.vectordb.vectorstore import VectorDB
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from schemas.models import get_milvus_settings


class VectorDBTest(TestCase):
    def setUp(self):
        self.settings = get_milvus_settings()
        self.embedding = MagicMock(spec=OpenAIEmbeddings)
        self.vector_db = VectorDB(settings=self.settings, embedding=self.embedding)

    @patch("llms.vectordb.vectorstore.connections.connect")
    def test_connect_to_milvus(self, mock_connect):
        """Milvus에 연결하는 테스트"""
        self.vector_db._connect_to_milvus()
        mock_connect.assert_called_once_with(
            alias=self.vector_db.alias,
            host=self.settings.milvus_host,
            port=self.settings.milvus_port,
        )

    @patch("llms.vectordb.vectorstore.connections.disconnect")
    def test_disconnect_from_milvus(self, mock_disconnect):
        """Milvus에서 연결을 끊는 테스트"""
        self.vector_db._disconnect_from_milvus()
        mock_disconnect.assert_called_once_with(alias=self.vector_db.alias)

    @patch("llms.vectordb.vectorstore.Milvus")
    def test_get_vectorstore_success(self, mock_milvus):
        """vectorstore를 가져오는 테스트"""
        vectorstore = self.vector_db._get_vectorstore("test_collection")
        mock_milvus.assert_called_once_with(
            embedding_function=self.embedding,
            connection_args={
                "host": self.settings.milvus_host,
                "port": self.settings.milvus_port,
            },
            collection_name="test_collection",
        )

    @patch("llms.vectordb.vectorstore.Collection")
    def test_get_collection_success(self, mock_collection):
        """collection을 가져오는 테스트"""
        collection = self.vector_db._get_collection("test_collection")
        mock_collection.assert_called_once_with("test_collection")

    @patch("llms.vectordb.vectorstore.utility")
    def test_drop_vectorstore_exists(self, mock_utility):
        """vectorstore의 collection을 삭제하는 테스트"""
        mock_utility.has_collection.return_value = True
        self.vector_db._drop_vectorstore("test_collection")
        mock_utility.drop_collection.assert_called_once_with("test_collection")

    @patch("llms.vectordb.vectorstore.utility")
    def test_exists_collection_true(self, mock_utility):
        """collection이 존재하는지 확인하는 테스트"""
        mock_utility.has_collection.return_value = True
        result = self.vector_db._exists("test_collection")
        self.assertTrue(result)

    @patch("llms.vectordb.vectorstore.utility")
    def test_exists_collection_false(self, mock_utility):
        """collection이 존재하지 않는지 확인하는 테스트"""
        mock_utility.has_collection.return_value = False
        result = self.vector_db._exists("test_collection")
        self.assertFalse(result)

    @patch("llms.vectordb.vectorstore.Collection")
    @patch("llms.vectordb.vectorstore.utility")
    def test_get_filtered_docs(self, mock_utility, mock_collection):
        """기존 문서를 필터링하는 테스트"""
        mock_utility.has_collection.return_value = True
        mock_collection_instance = MagicMock()
        mock_collection.return_value = mock_collection_instance

        docs = [Document(page_content="test_content", metadata={"key": "123"})]
        mock_collection_instance.query.return_value = []  # No existing docs

        filtered_docs = self.vector_db._get_filtered_docs("test_collection", docs)
        self.assertEqual(filtered_docs, docs)  # No existing docs, so all are returned

    @patch("llms.vectordb.vectorstore.split_docs")
    @patch("llms.vectordb.vectorstore.Milvus")
    def test_core_embedding_new_documents(self, mock_milvus, mock_split_docs):
        """새로운 문서를 임베딩하는 테스트"""
        mock_split_docs.return_value = [
            Document(page_content="test_content", metadata={"key": "123"})
        ]
        self.vector_db._get_filtered_docs = MagicMock(
            return_value=[
                Document(page_content="test_content", metadata={"key": "123"})
            ]
        )

        result = self.vector_db.core_embedding("test_collection", "dummy_path")
        self.assertTrue(result)

    @patch("llms.vectordb.vectorstore.split_docs")
    @patch("llms.vectordb.vectorstore.Milvus")
    def test_core_embedding_no_new_documents(self, mock_milvus, mock_split_docs):
        """새로운 문서가 기존 vectorstore에 있을 때 임베딩하는 테스트"""
        mock_split_docs.return_value = [
            Document(page_content="test_content", metadata={"key": "123"})
        ]
        self.vector_db._get_filtered_docs = MagicMock(return_value=[])

        result = self.vector_db.core_embedding("test_collection", "dummy_path")
        self.assertTrue(result)  # Should return True even if no new documents to embed

    @patch("llms.vectordb.vectorstore.Milvus")
    def test_get_retriever_success(self, mock_milvus):
        """retriever를 가져오는 테스트"""
        mock_vectorstore = MagicMock()
        mock_milvus.return_value = mock_vectorstore
        retriever = self.vector_db.get_retriever("test_collection")
        self.assertEqual(retriever, mock_vectorstore.as_retriever())
