from fastapi import FastAPI, Header, HTTPException

app = FastAPI(
    title="API de Seguridad con Tokens",
    description="Ejemplo educativo de autenticación basada en tokens",
    version="1.0"
)

# Usuario de ejemplo
USUARIO = "admin"
PASSWORD = "1234"

# Token de ejemplo
TOKEN = "abc123"


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando"
    }


@app.post("/login")
def login(usuario: str, password: str):

    if usuario == USUARIO and password == PASSWORD:

        return {
            "mensaje": "Autenticación correcta",
            "access_token": TOKEN,
            "token_type": "bearer"
        }

    raise HTTPException(
        status_code=401,
        detail="Usuario o contraseña incorrectos"
    )


@app.get("/estudiantes")
def estudiantes(authorization: str = Header(None)):

    if authorization != f"Bearer {TOKEN}":

        raise HTTPException(
            status_code=401,
            detail="Token inválido o ausente"
        )

    return {
        "mensaje": "Acceso autorizado",
        "estudiantes": [
            {
                "id": 1,
                "nombre": "Ana"
            },
            {
                "id": 2,
                "nombre": "Carlos"
            },
            {
                "id": 3,
                "nombre": "María"
            }
        ]
    }
