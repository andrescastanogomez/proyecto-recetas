# app/services/llm_service.py
import os
import json
import requests
from typing import List

def generar_receta_llm(ingredientes: List[str]) -> dict:
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "meta-llama/llama-3-8b-instruct:free")
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Si no tienes API Key configurada localmente aún, te dará esta receta segura
    if not api_key:
        return {
            "nombre": "Receta de Prueba (Falta LLM_API_KEY)",
            "ingredientes": ["Ingredientes provistos: " + ", ".join(ingredientes)],
            "pasos": "1. Configura tu API key de OpenRouter en las variables de entorno.\n2. Reinicia el contenedor.",
            "tiempo_estimado": "5 min",
            "dificultad": "Fácil"
        }

    ingredientes_str = ", ".join(ingredientes)
    
    # Diseñamos un prompt estricto para forzar al modelo a retornar solo JSON estructurado
    prompt = f"""
    Eres un chef profesional de alta cocina. Crea una receta única y coherente utilizando principalmente algunos o todos los siguientes ingredientes disponibles: {ingredientes_str}.
    Debes responder EXCLUSIVAMENTE con un objeto JSON válido, sin textos introductorios, sin saludos y sin bloques de código de markdown (no encierres la respuesta en ```json).
    La estructura interna del JSON debe ser exactamente esta:
    {{
        "nombre": "Nombre creativo del plato",
        "ingredientes": ["lista de ingredientes necesarios detallados con cantidades lógicas"],
        "pasos": "Pasos detallados de la preparación enumerados paso a paso de manera clara",
        "tiempo_estimado": "Tiempo total aproximado en minutos (ej: 25 min)",
        "dificultad": "Fácil, Media o Difícil"
    }}
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        resultado = response.json()
        
        texto_respuesta = resultado['choices'][0]['message']['content'].strip()
        
        # Limpieza por si el modelo ignora la instrucción y pone etiquetas markdown ```json
        if texto_respuesta.startswith("```"):
            texto_respuesta = texto_respuesta.replace("```json", "").replace("```", "").strip()
            
        # Parseamos el texto a un diccionario nativo de Python para validar el JSON
        receta_json = json.loads(texto_respuesta)
        return receta_json
        
    except Exception as e:
        # Mecanismo de contingencia elegante en caso de fallos de red o de formateo del modelo
        return {
            "nombre": "Combinado rápido del chef (Modo de Fallo)",
            "ingredientes": ingredientes,
            "pasos": f"Saltear los ingredientes disponibles en una sartén con un poco de aceite hasta que estén listos. Nota de error: {str(e)}",
            "tiempo_estimado": "15 min",
            "dificultad": "Fácil"
        }