# Generador de Recetas Inteligente con IA (RecetAI)

## 👥 Integrantes del Proyecto
* Andrés David Castaño Gómez - Backend Developer / DevOps
* Andrés Barbosa - Frontend & Integration Developer
* Andres  Serrano* - Frontend Developer / QA

## 🚀 Alcance del Proyecto
RecetAI es una aplicación web moderna diseñada para la gestión inteligente de inventarios de cocina y la automatización de recetas culinarias personalizadas utilizando Inteligencia Artificial. El sistema permite a los usuarios registrarse de forma segura, gestionar sus ingredientes disponibles en tiempo real y disparar consultas estructuradas a un Modelo de Lenguaje Grande (LLM) a través de la API de OpenRouter. La IA procesa exclusivamente los ingredientes provistos y retorna una receta coherente con porciones lógicas, tiempos estimados, nivel de dificultad y pasos detallados.

## 🛠️ Tecnologías Utilizadas
* **Backend:** FastAPI (Python 3.12)
* **Base de Datos:** MySQL 8.0 (Persistencia) / SQLite (Entorno de Pruebas en memoria)
* **ORM:** SQLAlchemy con PyMySQL
* **Seguridad:** Autenticación basada en Tokens JWT (Bcrypt para hashing de contraseñas)
* **Validación de Datos:** Pydantic V2
* **Pruebas de Software:** Pytest (6 pruebas unitarias integradas)
* **Contenerización y Orquestación:** Docker y Docker Compose
* **Integración de IA:** API de OpenRouter (Meta Llama 3)

## 🧪 Pruebas Unitarias
El proyecto cuenta con un conjunto de 6 pruebas automatizadas robustas que validan:
1. Esquemas de datos correctos en Pydantic.
2. Manejo de campos opcionales nulos en el inventario.
3. Mecanismos de contingencia y parseo estructurado del JSON del LLM.
4. Disponibilidad del endpoint raíz de la API.
5. Generación correcta de la documentación Swagger.
6. Protección y bloqueo de rutas privadas sin token de acceso.

Para ejecutar las pruebas localmente:
```bash
python3 -m pytest -v