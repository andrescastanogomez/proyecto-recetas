from app.services.llm_service import generar_prompt

def test_generacion_prompt():
    ingredientes = ["pollo", "arroz"]
    prompt = generar_prompt(ingredientes)

    assert "pollo" in prompt
    assert "arroz" in prompt