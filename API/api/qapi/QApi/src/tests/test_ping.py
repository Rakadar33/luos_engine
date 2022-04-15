from starlette.testclient import TestClient
from app.main import aqua_app

client = TestClient(aqua_app)

def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_path(test_app):
    api_version= ''

    response = test_app.get("/path")
    assert response.status_code == 200
    assert response.json() == {'message': 'Path', 'root_path': api_version}
