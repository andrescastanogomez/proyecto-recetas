from app.schemas.esquemas import IngredienteSchema

def test_ingrediente_valido():
    data = {"nombre": "pollo", "cantidad": 2}
    ingrediente = IngredienteSchema(**data)
    assert ingrediente.nombre == "pollo"