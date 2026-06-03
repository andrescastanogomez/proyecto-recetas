import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.schemas.esquemas import IngredienteCreate
from app.services.llm_service import generar_receta_llm

client = TestClient(app)

# ==========================================
# TEST 1: Validación Pydantic correcta
# ==========================================
def test_validacion_ingrediente_correcto():
    data = {"nombre": "Papa", "cantidad": "4 unidades"}
    ingrediente = IngredienteCreate(**data)
    assert ingrediente.nombre == "Papa"
    assert ingrediente.cantidad == "4 unidades"


# ==========================================
# TEST 2: Campo opcional
# ==========================================
def test_validacion_ingrediente_sin_cantidad():
    data = {"nombre": "Pimienta"}
    ingrediente = IngredienteCreate(**data)
    assert ingrediente.nombre == "Pimienta"
    assert ingrediente.cantidad is None


# ==========================================
# TEST 3: MOCK del LLM (IMPORTANTE PRO)
# ==========================================
def test_parseo_llm_estructura_segura():
    mock_response = {
        "nombre": "Arroz con Pollo",
        "ingredientes": ["Pollo", "Arroz"],
        "pasos": ["Paso 1", "Paso 2"]
    }

    with patch(
        "app.services.llm_service.generar_receta_llm",
        return_value=mock_response
    ):
        resultado = generar_receta_llm(["Pollo", "Arroz"])

        assert "nombre" in resultado
        assert "ingredientes" in resultado
        assert "pasos" in resultado
        assert isinstance(resultado["ingredientes"], list)


# ==========================================
# TEST 4: Endpoint root
# ==========================================
def test_endpoint_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Online"


# ==========================================
# TEST 5: Swagger docs
# ==========================================
def test_endpoint_docs_swagger():
    response = client.get("/docs")
    assert response.status_code == 200


# ==========================================
# TEST 6: Seguridad ruta protegida
# ==========================================
def test_seguridad_ruta_ingredientes_bloqueada():
    response = client.get("/api/ingredientes/")
    assert response.status_code == 401