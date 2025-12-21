from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_suggest_success():
    response = client.post(
    "/suggest",
    json = {"query": "¿Cómo cambio mi contraseña?"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "suggestion" in data
    assert "contraseña" in data["suggestion"].lower()

def test_suggest_no_match():
    response = client.post(
        "/suggest",
        json = {"query": "Como cocino una pizza?"}
    )
    
    assert response.status_code == 200
    data = response.json()

    assert "no se encontro" in data["suggestion"].lower()


def test_suggest_empty_query():
    response = client.post(
        "/suggest",
        json = {"query": "   "}
    )
    
    assert response.status_code == 422