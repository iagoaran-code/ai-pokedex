from src.loader import PokemonDataLoader
from src.engine import PokedexEngine

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
            "tell",
        ]

        if any(word in question.lower() for word in stats_keywords):
            hint = " (Note: 'is_legendary' is 0/1. 'generation' is 1-7.)"
            return self.engine.stats_agent.invoke(question + hint)["output"]
        else:
            return self.engine.lore_chain.invoke({"query": question})["result"]


if __name__ == "__main__":
    pokedex = PokedexOrchestrator()
    print(pokedex.get_answer("Name all Pokemon with the ability Iron Barbs"))
