🍳 Generador de Recetas Inteligente con IA (RecetAI)
👥 Integrantes del Proyecto
Andrés David Castaño Gómez - Backend Developer / DevOps
Andrés Barbosa - Frontend & Integration Developer
Andrés Serrano - Frontend Developer / QA
📌 Descripción

Aplicación web que permite gestionar ingredientes y generar recetas usando inteligencia artificial.

🚀 Tecnologías
FastAPI
MySQL
SQLAlchemy
JWT Auth
OpenRouter / LLM
Docker
Pytest
HTML + JavaScript
📦 Instalación
git clone https://github.com/usuario/proyecto-recetas.git
cd proyecto-recetas

python -m venv venv

# Windows:
venv\Scripts\activate

# Linux / Mac:
source venv/bin/activate

pip install -r requirements.txt
▶️ Ejecución
uvicorn app.main:app --reload

Abrir en el navegador:

http://localhost:8000
🧪 Tests
pytest -v

Incluye:

Tests de API
Tests JWT
Validaciones Pydantic
Mock del LLM
🧠 Arquitectura del Proyecto
app/
 ├── main.py
 ├── models/        # Base de datos (SQLAlchemy)
 ├── routers/       # Endpoints API
 ├── services/      # Lógica de negocio (IA, auth)
 ├── schemas/       # Validaciones Pydantic
 └── tests/         # Tests automatizados
🔌 Endpoints principales
Auth
POST /auth/register
POST /auth/login
Ingredientes
GET /api/ingredientes/
POST /api/ingredientes/
DELETE /api/ingredientes/
Recetas
POST /api/recetas/generar
GET /api/recetas/
DELETE /api/recetas/
🔐 Seguridad
JWT Authentication
Rutas protegidas
Hash de contraseñas con bcrypt
🐳 Docker (opcional)
docker-compose up --build
👨‍🎓 Proyecto académico

Proyecto desarrollado como parte de la asignatura de desarrollo web, integrando backend, IA y autenticación segura.