import os
import pytest
from dotenv import load_dotenv

# Load env variables for tests
load_dotenv()

@pytest.fixture(autouse=True)
def mock_env_vars():
    # Ensure key exists even if dummy, for pydantic validation
    if not os.getenv("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = "dummy_key"
