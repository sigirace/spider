from llms.modules import ChainModules
from langchain_core.documents import Document
from llms.vectordb.vectorstore import VectorDB


class Nodes:

    def __init__(
        self,
        vector_db: VectorDB,
        chain_modules: ChainModules,
        collection_name: str,
    ):
        self.vector_db = vector_db
        self.chain_modules = chain_modules
        self.collection_name = collection_name

    def retrieve(self, state):
        """
        Retrieve documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        print("****retrieve****")
        print("---RETRIEVE---")
        question = state["question"]
        if "retrieve_cnt" not in state:
            state["retrieve_cnt"] = 0
        retrieve_cnt = state["retrieve_cnt"]

        # Retrieval
        retriever = self.vector_db.get_retriever(collection_name=self.collection_name)
        documents = retriever.invoke(question)

        return {
            "documents": documents,
            "question": question,
            "retrieve_cnt": retrieve_cnt + 1,
        }

    def generate(self, state):
        """
        Generate answer using gpt knowledge

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("****generate****")
        print("---GENERATE(COMMON)---")
        question = state["question"]
        history = state["history"]

        generation = self.chain_modules.common(history, question)
        # RAG generation
        return {"question": question, "history": history, "generation": generation}

    def generate_rag(self, state):
        """
        Generate answer using vectorstore

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("****generate_rag****")
        print("---GENERATE RAG(VECTORSTORE)---")
        question = state["question"]
        documents = state["documents"]
        history = state["history"]
        if "hallucinate_cnt" not in state:
            state["hallucinate_cnt"] = 0
        hallucinate_cnt = state["hallucinate_cnt"]

        generation = self.chain_modules.rag(history, documents, question)
        # RAG generation
        return {
            "documents": documents,
            "question": question,
            "history": history,
            "generation": generation,
            "hallucinate_cnt": hallucinate_cnt + 1,
        }

    def generate_web_rag(self, state):
        """
        Generate answer using web search results

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("****generate_web_rag****")
        print("---GENERATE RAG(WEB SEARCH)---")
        question = state["question"]
        documents = state["documents"]
        history = state["history"]

        generation = self.chain_modules.web_rag(history, documents, question)
        # RAG generation
        return {
            "documents": documents,
            "question": question,
            "history": history,
            "generation": generation,
        }

    def grade_documents(self, state):
        """
        Determines whether the retrieved documents are relevant to the question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with only filtered relevant documents
        """
        print("****grade_documents****")
        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]

        # Score each doc
        filtered_docs = []
        for d in documents:
            score = self.chain_modules.retrieval_grader(d.page_content, question)
            grade = score.binary_score
            if grade == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
                continue
        return {
            "documents": filtered_docs,
            "question": question,
        }

    def transform_query(self, state):
        """
        Transform the query to produce a better question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a re-phrased question
        """
        print("****transform_query****")
        print("---TRANSFORM QUERY---")
        question = state["question"]
        documents = state["documents"]
        history = state["history"]

        # Re-write question
        better_question = self.chain_modules.re_write(history, question)
        return {
            "documents": documents,
            "question": better_question,
            "history": history,
        }

    def web_transform_query(self, state):
        """
        Transform the query to produce a better question for web search.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a re-phrased question
        """
        print("****web_transform_query****")
        print("---TRANSFORM QUERY---")
        question = state["question"]
        history = state["history"]

        # Re-write question
        better_question = self.chain_modules.re_write_for_web(history, question)
        return {"question": better_question, "history": history}

    def web_search(self, state):
        """
        Web search based on the re-phrased question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with appended web results
        """
        print("****web_search****")
        print("---WEB SEARCH---")
        question = state["question"]

        # Web search
        web_tool = self.chain_modules.web_search_tool()
        docs = web_tool.invoke(question)
        web_results = []
        for d in docs:
            web_results.append(
                Document(page_content=d["content"], metadata={"url": d["url"]})
            )

        return {"documents": web_results, "question": question}
