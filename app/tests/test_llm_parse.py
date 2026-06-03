from app.services.llm_service import parsear_respuesta

def test_parseo_llm():
    respuesta = '{"receta": "arroz con pollo"}'
    resultado = parsear_respuesta(respuesta)

    assert "receta" in resultado