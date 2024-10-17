from llms.graphs.nodes import ChainModules


class Edges:

    def __init__(
        self,
        chain_modules: ChainModules,
        max_hallucinate_cnt: int = 2,
        max_retrieve_cnt: int = 2,
    ):
        self.chain_modules = chain_modules
        self.max_hallucinate_cnt = max_hallucinate_cnt
        self.max_retrieve_cnt = max_retrieve_cnt

    def route_question(self, state):
        """
        Route question to web search or RAG.

        Args:
            state (dict): The current graph state

        Returns:
            str: Next node to call
        """
        print("****route_question****")
        print("1. ---ROUTE QUESTION---")
        question = state["question"]
        history = state["history"]
        vector_router_source = self.chain_modules.router(history, question)

        if vector_router_source.datasource == "common":
            print("2. ---DECIDE TO COMMAN CHAT OR WEB SEARCH---")
            web_router_source = self.chain_modules.web_router(history, question)
            if web_router_source.datasource == "common":
                print("3. ---ROUTE QUESTION TO COMMON CHAT---")
                return "common"
            elif web_router_source.datasource == "web_search":
                print("3. ---ROUTE QUESTION TO WEB SEARCH---")
                return "web_search"
        elif vector_router_source.datasource == "vectorstore":
            print("2. ---ROUTE QUESTION TO RAG---")
            return "vectorstore"

    def decide_to_generate(self, state):
        """
        Determines whether to generate an answer, or re-generate a question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Binary decision for next node to call
        """
        print("****decide_to_generate****")
        print("1. ---ASSESS GRADED DOCUMENTS---")
        filtered_documents = state["documents"]
        retrieve_cnt = state["retrieve_cnt"]

        if not filtered_documents:
            if retrieve_cnt > self.max_retrieve_cnt:
                # 웹서치
                return "infinite"
            else:
                # All documents have been filtered check_relevance
                # We will re-generate a new query
                print(
                    "2. ---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
                )
                return "transform_query"
        else:
            # We have relevant documents, so generate answer
            print("2. ---DECISION: GENERATE---")
            return "generate_rag"

    def check_hallucination(self, state):
        """
        Determines whether the generation is grounded in the document and answers question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Decision for next node to call
        """
        print("****check_hallucination****")
        documents = state["documents"]
        generation = state["generation"]
        history = state["history"]
        hallucinate_cnt = state["hallucinate_cnt"]

        score = self.chain_modules.hallucination_grader(history, documents, generation)
        grade = score.multiple_score

        if grade == "yes":
            ## 끝
            return "useful"
        else:
            ## 재생성
            if hallucinate_cnt > self.max_hallucinate_cnt:
                return "infinite"
            else:
                return "not useful"
