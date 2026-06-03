import os
import json
from typing import List

from google import genai


def generar_receta_llm(ingredientes: List[str]) -> dict:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "nombre": "Receta sugerida",
            "ingredientes": ingredientes,
            "pasos": (
                "1. Lava y prepara los ingredientes.\n"
                "2. Combínalos adecuadamente.\n"
                "3. Cocina durante 15 minutos.\n"
                "4. Sirve y disfruta."
            ),
            "tiempo_estimado": "15 min",
            "dificultad": "Fácil"
        }

    prompt = f"""
Usa únicamente estos ingredientes:

{", ".join(ingredientes)}

Genera una receta REAL, detallada y útil.

Devuelve EXCLUSIVAMENTE JSON válido con este formato:

{{
    "nombre": "Nombre de la receta",
    "ingredientes": [
        "ingrediente 1",
        "ingrediente 2"
    ],
    "pasos": "1. Paso uno\\n2. Paso dos\\n3. Paso tres\\n4. Paso cuatro",
    "tiempo_estimado": "20 min",
    "dificultad": "Fácil"
}}

No agregues markdown.
No agregues comentarios.
No agregues texto adicional.
"""

    try:

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        contenido = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        print("RESPUESTA GEMINI:")
        print(contenido)

        receta = json.loads(contenido)

        return {
            "nombre": receta.get(
                "nombre",
                "Receta generada"
            ),
            "ingredientes": receta.get(
                "ingredientes",
                ingredientes
            ),
            "pasos": receta.get(
                "pasos",
                "No se generaron pasos."
            ),
            "tiempo_estimado": receta.get(
                "tiempo_estimado",
                "20 min"
            ),
            "dificultad": receta.get(
                "dificultad",
                "Media"
            )
        }

    except Exception as e:

        print("ERROR GEMINI:", str(e))

        return {
            "nombre": "Error IA",
            "ingredientes": ingredientes,
            "pasos": f"Error generando receta: {str(e)}",
            "tiempo_estimado": "-",
            "dificultad": "-"
        }