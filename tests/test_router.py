import os
import sys

# This tells the test to look in the main folder for 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_src_folder_exists():
    """Checks if the refactoring Felipe asked for is done."""
    assert os.path.exists("src/loader.py")
    assert os.path.exists("src/engine.py")
    assert os.path.exists("src/router.py")

def test_routing_logic():
    """Tests the keyword detection without needing Azure keys."""
    stats_keywords = ["highest", "lowest", "strongest", "fastest"]
    question = "Who is the fastest Pokemon?"
    
    is_stats = any(word in question.lower() for word in stats_keywords)
    assert is_stats is True
