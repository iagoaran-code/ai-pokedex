import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Creates vector database, LLM, and Chains
class PokedexEngine:
    """Handles the AI models and Retrieval logic."""

    def __init__(self, df, docs):
        self.df = df
        self.docs = docs
        self._setup_models()
        self._setup_tools()

    def _setup_models(self):
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment="text-embedding-3-small", openai_api_version="2024-02-01"
        )
        self.llm = AzureChatOpenAI(
            azure_deployment="praxis-gpt4o-mini-context-deployment",
            api_version="2024-12-01-preview",
            temperature=0,
        )

    def _setup_tools(self):
        vector_db = Chroma.from_documents(
            documents=self.docs, embedding=self.embeddings
        )
        self.lore_chain = RetrievalQA.from_chain_type(
            llm=self.llm, retriever=vector_db.as_retriever(search_kwargs={"k": 3})
        )
        self.stats_agent = create_pandas_dataframe_agent(
            self.llm, self.df, allow_dangerous_code=True, agent_type="openai-functions"
        )
