import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from src.loader import PokemonDataLoader
from src.router import PokedexOrchestrator


# -------------------
# LOADER TESTS
# -------------------

def test_get_weaknesses():
    data = {
        "name": ["pikachu"],
        "type1": ["electric"],
        "type2": [""],
        "classfication": ["mouse"],
        "against_water": [2],
        "against_fire": [0.5],
    }

    df = pd.DataFrame(data)
    loader = PokemonDataLoader.__new__(PokemonDataLoader)
    loader.df = df

    row = df.iloc[0]
    weaknesses = loader._get_weaknesses(row)

    assert "water" in weaknesses
    assert "fire" not in weaknesses


def test_prepare_documents():
    data = {
        "name": ["pikachu"],
        "type1": ["electric"],
        "type2": [""],
        "classfication": ["mouse"],
        "against_water": [2],
    }

    df = pd.DataFrame(data)
    loader = PokemonDataLoader.__new__(PokemonDataLoader)
    loader.df = df

    docs = loader.prepare_documents()

    assert len(docs) == 1
    assert "pikachu" in docs[0].page_content.lower()


# -------------------
# ROUTER TESTS
# -------------------

@patch("src.router.PokedexEngine")
@patch("src.router.PokemonDataLoader")
def test_stats_branch(mock_loader, mock_engine):
    mock_loader.return_value.df = "df"
    mock_loader.return_value.prepare_documents.return_value = ["doc"]

    mock_engine_instance = MagicMock()
    mock_engine.return_value = mock_engine_instance
    mock_engine_instance.stats_agent.invoke.return_value = {"output": "stats"}

    orch = PokedexOrchestrator()
    result = orch.get_answer("highest attack")

    assert result == "stats"


@patch("src.router.PokedexEngine")
@patch("src.router.PokemonDataLoader")
def test_lore_branch(mock_loader, mock_engine):
    mock_loader.return_value.df = "df"
    mock_loader.return_value.prepare_documents.return_value = ["doc"]

    mock_engine_instance = MagicMock()
    mock_engine.return_value = mock_engine_instance
    mock_engine_instance.lore_chain.invoke.return_value = {"result": "lore"}

    orch = PokedexOrchestrator()
    result = orch.get_answer("pikachu story")

    assert result == "lore"


# -------------------
# KEYWORD COVERAGE
# -------------------

@pytest.mark.parametrize("question", [
    "highest attack",
    "lowest speed",
    "strongest pokemon",
    "what is the fastest"
])
@patch("src.router.PokedexEngine")
@patch("src.router.PokemonDataLoader")
def test_keywords(mock_loader, mock_engine, question):
    mock_loader.return_value.df = "df"
    mock_loader.return_value.prepare_documents.return_value = ["doc"]

    mock_engine_instance = MagicMock()
    mock_engine.return_value = mock_engine_instance
    mock_engine_instance.stats_agent.invoke.return_value = {"output": "ok"}

    orch = PokedexOrchestrator()
    result = orch.get_answer(question)

    assert result == "ok"


# -------------------
# ERROR TEST
# -------------------

def test_loader_file_not_found():
    with pytest.raises(Exception):
        PokemonDataLoader("fake.csv")
        pd.read_csv("non_existent_file.csv")
    except FileNotFoundError:
        pass
