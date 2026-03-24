import os
import pandas as pd
from langchain_core.documents import Document

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
