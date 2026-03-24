import pytest
from src.router import PokedexOrchestrator

def test_complex_filtering_query():
    pokedex = PokedexOrchestrator(csv_path="pokemon.csv")
    
    question = "Name all pokemon with more than 100 speed, but less than 50 attack"
    
    response = pokedex.get_answer(question)
    
    assert isinstance(response, str)
    
    error_phrases = ["error", "could not find", "not available"]
    assert not any(phrase in response.lower() for phrase in error_phrases),

    assert len(response) > 10
