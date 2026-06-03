from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generar_receta_endpoint():
    response = client.post(
        "/api/recetas/generar",
        json={"ingredientes": ["pollo", "arroz"]}
    )

    assert response.status_code in [200, 201]