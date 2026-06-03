from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ==========================================
# TEST 1: LOGIN Y GENERACIÓN DE TOKEN JWT
# ==========================================
def test_login_obtiene_token():
    data = {
        "username": "testuser",
        "password": "123456"
    }

    response = client.post("/auth/login", data=data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# ==========================================
# TEST 2: ACCESO A RUTA PROTEGIDA CON TOKEN
# ==========================================
def test_ruta_protegida_con_token():
    # Login primero
    login_data = {
        "username": "testuser",
        "password": "123456"
    }

    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get("/api/ingredientes/", headers=headers)

    # Ya no debe ser 401 si el token es válido
    assert response.status_code in [200, 404]