import unittest
from fastapi.testclient import TestClient
from app.main import app

# TestClient simula llamadas HTTP a la API sin levantar un servidor real
client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_suggest_basic(self):
        """
        Verifica que /suggest responda 200 y devuelva 'suggestion'.
        """
        payload = {"query": "¿Cómo cambio mi contraseña?"}
        resp = client.post("/suggest", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("suggestion", data)
        self.assertTrue(len(data["suggestion"]) > 0)

    def test_history_returns_list(self):
        """
        Asegura que /history devuelva una lista con al menos un elemento
        después de haber invocado /suggest.
        """
        client.post("/suggest", json={"query": "¿Cuál es el horario de atención?"})
        resp = client.get("/history")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIn("query", data[0])
        self.assertIn("suggestion", data[0])

    def test_validation_empty_query(self):
        """
        Valida que una 'query' vacía sea rechazada por Pydantic/FastAPI.
        FastAPI retorna 422 Unprocessable Entity.
        """
        resp = client.post("/suggest", json={"query": "   "})
        self.assertEqual(resp.status_code, 422)

    def test_add_kb_item(self):
        """
        Verifica que podamos agregar una nueva pregunta a la base de conocimiento
        o recibir 409 si ya existe.
        """
        resp = client.post("/kb", json={"pregunta": "¿Dónde veo mis pedidos?", "respuesta": "En la sección 'Mis pedidos' del panel."})
        self.assertIn(resp.status_code, (200, 409))

if __name__ == "__main__":
    unittest.main()
