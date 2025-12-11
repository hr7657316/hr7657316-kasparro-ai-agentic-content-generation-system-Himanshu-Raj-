import pytest
import os
from src.agents.data_parser_agent import DataParserAgent

import time

@pytest.mark.skipif(not os.getenv("GOOGLE_API_KEY"), reason="No API key found")
def test_data_parser_real_integration():
    """
    Real integration test hitting the Gemini API with retry logic.
    """
    agent = DataParserAgent()
    input_data = {
        "Product Name": "Test Cream",
        "Price": "$50",
        "Benefits": "Moisturizing"
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = agent.run(input_data)
            break
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e) and attempt < max_retries - 1:
                print(f"quota exceeded, retrying in 5s... (attempt {attempt+1})")
                time.sleep(5)
            else:
                raise e
    
    # Assertions based on expected schema
    assert result["name"] is not None
    assert result["price"] is not None
    assert isinstance(result, dict)

