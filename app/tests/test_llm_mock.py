from unittest.mock import patch
from app.services.llm_service import generar_receta_llm

# ==========================
# TEST CON MOCK DEL LLM
# ==========================
@patch("app.services.llm_service.generar_receta_llm")
def test_llm_mock(mock_llm):

    mock_llm.return_value = {
        "nombre": "Arroz con Pollo Mock",
        "ingredientes": ["pollo", "arroz"],
        "pasos": ["mezclar", "cocinar"],
        "tiempo": "30 min",
        "dificultad": "fácil"
    }

    resultado = generar_receta_llm(["pollo", "arroz"])

    assert resultado["nombre"] == "Arroz con Pollo Mock"
    assert isinstance(resultado["ingredientes"], list)