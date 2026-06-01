import requests
from typing import Literal
from flask import Response

def make_request(url: str, method: Literal["GET", "POST", "PUT", "DELETE"], data: dict = {}) -> requests.Response:
    if method == "POST":
        response = requests.post(url, json=data)
    elif method == "PUT":
        response = requests.put(url, json=data)
    elif method == "DELETE":
        response = requests.delete(url)
    else:
        response = requests.get(url)
    return response

def make_cookie_response(res: Response, token: str):
    """
    Crea una cookie de sesión segura en la respuesta dada, con el token proporcionado.
    El nombre de la cookie es "session_token"
    """
    res.set_cookie(
        key="session_token",
        value=token,
        httponly=True,       # Bloquea JS (Evita robos por XSS)
        samesite="Lax",      # Permite que funcione en localhost entre puertos distintos
        secure=False,        # FALSE porque estás usando HTTP normal en tu PC
        max_age=3600         # Tiempo de vida en segundos (1 hora)
    )