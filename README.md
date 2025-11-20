# 📊 API Gateway Service

Servicio encargado de:
- Es la única puerta de entrada para el frontend móvil.

- Valida Firebase ID Tokens.

- Genera un JWT interno (RS256) para llamar a los microservicios.

- Orquesta llamadas a:

    - backend-profile-service

    - backend-education-service

    - backend-progress-service

    - ai-service

Link del repositorio en GitHub: https://github.com/Creative-Craft-UPC/api-gateway

---

## Clonar el Repositorio

```bash
git clone https://github.com/Creative-Craft-UPC/api-gateway.git
cd social_fun
```

## 🧱 Stack

- Python 3.11
- FastAPI
- Python 3.11
- FastAPI
- Firebase Admin SDK
- httpx (para consumo de microservicios)
- PyJWT (firma de token interno)
- python-dotenv

---

## 📁 Estructura básica

- `main.py` → punto de entrada FastAPI
- `routes/` → rutas HTTP
- `auth/internal_dep.py` → validación de token interno (JWT RS256)
- `requirements.txt` → dependencias de Python
- `Dockerfile` → build de imagen
- `schemas` → Esquemas principales del servicio 
- `services` → Consultas a los microservicios

---
## ⚙ Variables de entorno
### Firebase admin
FIREBASE_SA_PATH=secrets/firebase-sa.json

### Claves interna BFF (JWT RS256)
PRIVATE_KEY_PATH=secrets/bff_private.pem

### URLs de microservicios (en local)
- PROFILE_SERVICE_URL=http://localhost:8001
- EDUCATION_SERVICE_URL=http://localhost:8002
- PROGRESS_SERVICE_URL=http://localhost:8004
- AI_SERVICE_URL=http://localhost:8003


## Ejecución:
### 🚀 Ejecutar en local (sin Docker)

1. Crear entorno virtual y activalo:

    python -m venv gatewayContext

    gatewayContext/Scripts/activate ---> Windows

    source gatewayContext/bin/activate ---> Linux/Mac

2. Instalar dependencias:

    pip install -r requirements.txt

3. Ejecutar:

    uvicorn main:app --reload --port 8000

### 🐳 Ejecutar con Docker
#### Build

    docker build -t api-gateway .

#### Run

    docker run -p 8000:8000 \
      -e FIREBASE_SA_PATH=/app/secrets/firebase-sa.json \
      -e PRIVATE_KEY_PATH=/app/secrets/bff_private.pem \
      -e PROFILE_SERVICE_URL=http://host.docker.internal:8001 \
      -e EDUCATION_SERVICE_URL=http://host.docker.internal:8002 \
      -e PROGRESS_SERVICE_URL=http://host.docker.internal:8004 \
      -e AI_SERVICE_URL=http://host.docker.internal:8003 \
      api-gateway