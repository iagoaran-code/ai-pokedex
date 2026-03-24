from src.router import PokedexOrchestrator

if __name__ == "__main__":
    pokedex = PokedexOrchestrator()
    print(pokedex.get_answer("Name all Pokemon with the ability Iron Barbs"))
