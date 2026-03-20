import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_core.documents import Document

load_dotenv()


# Loading the CSV
class PokemonDataLoader:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def _get_weaknesses(self, row):
        return ", ".join(
            [
                col.replace("against_", "")
                for col in self.df.columns
                if col.startswith("against_") and row[col] > 1
            ]
        )

    def prepare_documents(self):
        docs = []
        for _, row in self.df.iterrows():
            text = (
                f"Name: {row['name']}\nType: {row['type1']} {row['type2']}\n"
                f"Weaknesses: {self._get_weaknesses(row)}\n"
                f"Description: {row['classfication']}"
            )
            docs.append(Document(page_content=text, metadata={"name": row["name"]}))
        return docs


# Creates vector DB, LLM, and Chains
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


# Decides which tool to use
class PokedexOrchestrator:
    def __init__(self, csv_path="pokemon.csv"):
        loader = PokemonDataLoader(csv_path)
        documents = loader.prepare_documents()
        self.engine = PokedexEngine(loader.df, documents)

    def get_answer(self, question):
        stats_keywords = [
            "highest",
            "lowest",
            "strongest",
            "fastest",
            "average",
            "total",
            "count",
            "name",
            "what",
            "which",
        ]

        if any(word in question.lower() for word in stats_keywords):
            hint = " (Note: 'is_legendary' is 0/1. 'generation' is 1-7.)"
            return self.engine.stats_agent.invoke(question + hint)["output"]
        else:
            return self.engine.lore_chain.invoke({"query": question})["result"]


if __name__ == "__main__":
    pokedex = PokedexOrchestrator()
    print(pokedex.get_answer("Name all Pokemon with the ability Iron Barbs"))
