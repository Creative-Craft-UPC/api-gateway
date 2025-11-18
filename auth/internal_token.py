# app/auth/internal_token.py
import os, time, jwt

# Sugerencia: guardar el PEM en una env var; alternativo: leer archivo
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH", "secrets/bff_private.pem")

with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()

def mint_internal_token(user_id: str, ttl_seconds: int = 300) -> str:
    now = int(time.time())
    payload = {
        "iss": "bff.socialfun",
        "sub": user_id,  # el UID del usuario
        "iat": now,
        "exp": now + ttl_seconds,
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
