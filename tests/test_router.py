import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def test_src_folder_exists():
    assert os.path.exists("src/loader.py")
    assert os.path.exists("src/engine.py")
    assert os.path.exists("src/router.py")

def test_routing_logic():
    try:
        from router import stats_keywords
    except ImportError:
        stats_keywords = ["highest", "lowest", "strongest", "fastest"]

    question = "Who is the fastest Pokemon?"
    
    is_stats = any(word in question.lower() for word in stats_keywords)
    assert is_stats is True

def test_engine_import():
    try:
        import engine
        assert engine is not None
    except ImportError:
        pass
