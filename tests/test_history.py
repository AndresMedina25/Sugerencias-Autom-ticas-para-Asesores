from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_history_initially_empty():
    response = client.get("/history")
    
    assert response.status_code == 200
    assert response.json() == []
    
def test_history_after_suggestions():
    client.post("/suggest", json={"query": "¿Cómo cambio mi contraseña?"})
    client.post("/suggest", json={"query": "¿Cuál es el horario de atención?"})
    
    response = client.get("/history")
    data = response.json()
    
    assert len(data) >= 2 
    assert "query" in data[0]
    assert "suggestion" in data[0]