# app/tests/test_proyecto.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.esquemas import IngredienteCreate
from app.services.llm_service import generar_receta_llm

client = TestClient(app)

# Test 1: Validación de Esquema de Pydantic con datos válidos
def test_validacion_ingrediente_correcto():
    data = {"nombre": "Papa", "cantidad": "4 unidades"}
    ingrediente = IngredienteCreate(**data)
    assert ingrediente.nombre == "Papa"
    assert ingrediente.cantidad == "4 unidades"

# Test 2: Validación de Esquema permitiendo campos opcionales nulos
def test_validacion_ingrediente_sin_cantidad():
    data = {"nombre": "Pimienta"}
    ingrediente = IngredienteCreate(**data)
    assert ingrediente.nombre == "Pimienta"
    assert ingrediente.cantidad is None

# Test 3: Simulación y verificación del parseo del servicio LLM (Formato Fallback)
def test_parseo_llm_estructura_segura():
    resultado = generar_receta_llm(["Pollo", "Arroz"])
    assert "nombre" in resultado
    assert "ingredientes" in resultado
    assert "pasos" in resultado
    assert isinstance(resultado["ingredientes"], list)

# Test 4: Verificación de disponibilidad del Endpoint Raíz de la API
def test_endpoint_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Online"

# Test 5: Verificación de la autogeneración de documentación Swagger (Requisito técnico)
def test_endpoint_docs_swagger():
    response = client.get("/docs")
    assert response.status_code == 200

# Test 6: Verificación de protección de rutas privadas (Debe responder 401 Unauthorized sin Token)
def test_seguridad_ruta_ingredientes_bloqueada():
    response = client.get("/api/ingredientes/")
    assert response.status_code == 401