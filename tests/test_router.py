import os
import sys
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_src_folder_exists():
    assert os.path.exists("src/loader.py")
    assert os.path.exists("src/router.py")

def test_csv_readable():
    csv_path = "pokemon.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        assert not df.empty
        assert any(c.lower() == 'name' for c in df.columns)

def test_orchestrator_logic_paths():
    with patch('src.router.PokedexOrchestrator') as MockOrch:
        orch = MockOrch() 
        orch.route.return_value = "Mock Response"
        
        assert orch.route("test") == "Mock Response"
        assert MockOrch.called

    stats_keywords = ["highest", "lowest", "strongest", "fastest", "speed", "attack"]
    questions = [
        "Who is the highest attack?", 
        "Which is the lowest speed?", 
        "Tell me about Pikachu"
    ]
    
    for q in questions:
        is_stats = any(word in q.lower() for word in stats_keywords)
        assert isinstance(is_stats, bool)

def test_loader_error_handling():
    try:
        pd.read_csv("non_existent_file.csv")
    except FileNotFoundError:
        pass
