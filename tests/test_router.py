import os
import sys
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.router import PokedexOrchestrator
from src.loader import PokemonDataLoader

def test_src_folder_exists():
    assert os.path.exists("src/loader.py")
    assert os.path.exists("src/engine.py")
    assert os.path.exists("src/router.py")

def test_routing_logic_basic():
    orchestrator = PokedexOrchestrator(MagicMock(), MagicMock())
    question = "Who is the fastest Pokemon?"
    assert orchestrator.is_stats_question(question) is True

def test_router_edge_cases():
    orchestrator = PokedexOrchestrator(MagicMock(), MagicMock())
    
    assert orchestrator.is_stats_question("Tell me a story about Mewtwo") is False
    
    assert orchestrator.is_stats_question("") is False

def test_loader_unit():
    loader = PokemonDataLoader(csv_path="pokemon.csv")
    assert loader.csv_path == "pokemon.csv"

def test_loader_error_handling():
    loader = PokemonDataLoader(csv_path="non_existent.csv")
    with pytest.raises(FileNotFoundError):
        loader.load_data()
