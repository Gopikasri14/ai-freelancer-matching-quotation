import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is discoverable by pytest
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app
from app.core.config import get_settings, Settings


@pytest.fixture(scope="session")
def client() -> TestClient:
    """TestClient fixture reusing the FastAPI app instance."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Settings fixture."""
    return get_settings()
