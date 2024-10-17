from langgraph.graph import END, StateGraph, START
from schemas.models import GraphState
from llms.graphs.nodes import Nodes
from llms.graphs.edges import Edges


class LangGraph:
    def __init__(
        self,
        nodes: Nodes,
        edges: Edges,
    ):
        self.nodes = nodes
        self.edges = edges
        self.workflow = StateGraph(GraphState)
        self.setup_workflow()
        self.app = self.workflow.compile()

    def setup_workflow(self):
        """
        Sets up the nodes and edges for the workflow.
        """
        self.set_nodes()
        self.set_edges()

    def set_nodes(self):
        """
        Define the nodes
        """
        self.workflow.add_node("retrieve", self.nodes.retrieve)  # Retrieve
        self.workflow.add_node("web_search", self.nodes.web_search)  # Web search
        self.workflow.add_node(
            "grade_documents", self.nodes.grade_documents
        )  # Grade documents
        self.workflow.add_node("generate_rag", self.nodes.generate_rag)  # Generate RAG
        self.workflow.add_node("generate", self.nodes.generate)  # Generate
        self.workflow.add_node(
            "generate_web_rag", self.nodes.generate_web_rag
        )  # Generate Web RAG
        self.workflow.add_node(
            "transform_query", self.nodes.transform_query
        )  # Transform query
        self.workflow.add_node(
            "web_transform_query", self.nodes.web_transform_query
        )  # Web transform query

    def set_edges(self):
        """
        Define the workflow edges and conditions
        """
        self.workflow.add_conditional_edges(
            START,
            self.edges.route_question,
            {
                "common": "generate",
                "web_search": "web_transform_query",
                "vectorstore": "retrieve",
            },
        )
        self.workflow.add_edge("generate", END)
        self.workflow.add_edge("retrieve", "grade_documents")
        self.workflow.add_conditional_edges(
            "grade_documents",
            self.edges.decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate_rag": "generate_rag",
                "infinite": "web_transform_query",
            },
        )
        self.workflow.add_edge("transform_query", "retrieve")
        self.workflow.add_conditional_edges(
            "generate_rag",
            self.edges.check_hallucination,
            {
                "useful": END,
                "not useful": "generate_rag",
                "infinite": "web_transform_query",
            },
        )
        self.workflow.add_edge("web_transform_query", "web_search")
        self.workflow.add_edge("web_search", "generate_web_rag")
        self.workflow.add_edge("generate_web_rag", END)

    def __call__(self, inputs: dict) -> dict:
        """
        Execute the precompiled workflow with the given inputs.
        """
        for output in self.app.stream(inputs):
            print("output", output)
            for key, value in output.items():
                print(f"Node : {key}")

        return value
