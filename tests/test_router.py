import os
import sys
import pytest
from unittest.mock import MagicMock
import pandas as pd

# Fix pathing so it works in GitHub Actions and local
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.router import PokedexOrchestrator
from src.loader import PokemonDataLoader

def get_orchestrator():
    """Helper to handle whether your class takes 1 or 2 arguments."""
    mock_engine = MagicMock()
    mock_loader = MagicMock()
    try:
        # Try passing both (Engine, Loader)
        return PokedexOrchestrator(mock_engine, mock_loader)
    except TypeError:
        # Fallback if it only takes (Engine)
        return PokedexOrchestrator(mock_engine)

def test_src_folder_exists():
    assert os.path.exists("src/loader.py")
    assert os.path.exists("src/engine.py")
    assert os.path.exists("src/router.py")

def test_routing_logic_basic():
    orchestrator = get_orchestrator()
    question = "Who is the fastest Pokemon?"
    assert orchestrator.is_stats_question(question) is True

def test_router_edge_cases():
    orchestrator = get_orchestrator()
    assert orchestrator.is_stats_question("Tell me a story") is False
    assert orchestrator.is_stats_question("") is False

def test_loader_instantiation():
    loader = PokemonDataLoader(csv_path="pokemon.csv")
    assert loader is not None

def test_loader_error_handling():
    # We use a completely fake name to trigger the error handling
    loader = PokemonDataLoader(csv_path="missing_file_for_test.csv")
    with pytest.raises((FileNotFoundError, Exception)):
        loader.load_data()

def test_csv_readable():
    """Checks if the actual CSV is present and readable in the root."""
    assert os.path.exists("pokemon.csv")
    df = pd.read_csv("pokemon.csv")
    assert not df.empty
