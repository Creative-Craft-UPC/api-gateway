# app/auth/internal_token.py
import os, time, jwt

# Sugerencia: guardar el PEM en una env var; alternativo: leer archivo
PRIVATE_KEY = os.environ["PRIVATE_KEY"]

def mint_internal_token(user_id: str, ttl_seconds: int = 300) -> str:
    now = int(time.time())
    payload = {
        "iss": "bff.socialfun",
        "sub": user_id,  # el UID del usuario
        "iat": now,
        "exp": now + ttl_seconds,
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
