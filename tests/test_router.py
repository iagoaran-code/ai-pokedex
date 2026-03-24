import os
import sys
import pytest

# This tells Python where to find your 'src' folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# 1. IMPORT your actual functions/classes here
from router import your_routing_function 

def test_src_folder_exists():
    assert os.path.exists("src/loader.py")
    assert os.path.exists("src/engine.py")
    assert os.path.exists("src/router.py")

def test_routing_logic():
    question = "Who is the fastest Pokemon?"
    
    # 2. CALL the actual function from your src code
    # This is what triggers the coverage tracker!
    result = your_routing_function(question) 
    
    assert result == "expected_output_for_stats"
