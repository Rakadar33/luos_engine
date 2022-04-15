import pytest
from starlette.testclient import TestClient

from app.main import aqua_app

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(aqua_app)
    yield client  # testing happens here