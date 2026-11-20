from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "ok"

def test_fraction_question():
    response = client.post("/api/ask", json={"question": "Help me understand fractions"})
    assert response.status_code == 200
    assert response.json()["gadget"] == "math"

def test_unknown_question():
    response = client.post("/api/ask", json={"question": "How does something unknown work?"})
    assert response.status_code == 200
    assert response.json()["source"] == "curated"

def test_quiz():
    response = client.post("/api/quiz", json={"topic": "science", "count": 3})
    assert response.status_code == 200
    assert len(response.json()["questions"]) == 3

def test_input_validation():
    assert client.post("/api/ask", json={"question": ""}).status_code == 422
