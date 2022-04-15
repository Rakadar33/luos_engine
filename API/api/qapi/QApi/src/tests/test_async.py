from starlette.testclient import TestClient
from app.main import aqua_app

client = TestClient(aqua_app)


'''
def test_test(test_app):
    response = test_app.get("/wip")
    assert response.status_code == 200
    assert response.json() == {"get" : "wip"}
'''

def test_rtb(test_app):
    response = test_app.get("/rtb")
    assert response.status_code == 200    


def test_platform(test_app):
    json= {"title": "Hello", "description": "bla"}
    
    response = test_app.post("/platform/", json= json )
    
    assert response.status_code == 200
    assert response.json() == json
