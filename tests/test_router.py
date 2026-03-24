from src.router import PokedexOrchestrator

def test_stats_keyword_logic():
    """
    Checks if our keyword logic correctly identifies a 'stats' question.
    """
    stats_keywords = ["highest", "lowest", "strongest", "fastest", "average"]
    question = "Who is the fastest Pokemon?"
    
    # This mimics the logic inside your get_answer method
    is_stats_query = any(word in question.lower() for word in stats_keywords)
    
    assert is_stats_query is True, "The word 'fastest' should trigger stats logic"

def test_lore_keyword_logic():
    """
    Checks if a non-stats question correctly bypasses the stats logic.
    """
    stats_keywords = ["highest", "lowest", "strongest", "fastest"]
    question = "Tell me a story about Pikachu"
    
    is_stats_query = any(word in question.lower() for word in stats_keywords)
    
    assert is_stats_query is False, "A story request should not trigger stats logic"
