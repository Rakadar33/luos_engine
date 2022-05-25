from starlette.testclient import TestClient
from app.main import aqua_app

client = TestClient(aqua_app)

'''
def test_regression(test_app):
    response = test_app.post("/nreg")
    assert response.status_code == 200
    assert response.json() == {"result": "HELLO"}
'''

'''
def test_create_non_regression(test_app):
    response = test_app.post("/nreg/",
                            headers={"X-Token": "Pluto"},
                            json={"title": "Hello", "description": "Empty"})
    assert response.status_code == 307
    assert response.json() == "hello.sh"
'''

def test_create_non_regression(test_app):
    response = test_app.get("/nreg/")
    assert response.status_code == 200
    #response = test_app.post("/nreg/", json={"title": "Hello"})
    #assert response.status_code == 307
    #assert response.json() == "hello.sh"