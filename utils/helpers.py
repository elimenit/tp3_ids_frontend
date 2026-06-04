import requests
from typing import Literal
from flask import Response, flash
import json

def make_request(
        url: str, 
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"], 
        data: dict = {}, 
        headers: dict = {}, 
        token: str = ""
    ) -> requests.Response:
    """
    Realiza una solicitud HTTP a la URL. 
    ### Args:
        - url
        - method
        - data: Diccionario con los datos a enviar (para POST/PUT)
        - headers: Diccionario con headers adicionales
        - token: Token JWT para enviar. Si se proporciona, se agrega al header Authorization como Bearer.
    ### Returns:
        - Objeto Response de requests
    """
    final_headers = dict(headers)
    if token:
        final_headers.update(get_bearer_headers(token))

    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=final_headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=final_headers)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers=final_headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=final_headers)
        else:
            response = requests.get(url, headers=final_headers)
    except requests.exceptions.ConnectionError:
        raise Exception("No se pudo conectar con el servidor") 

    return response

def get_bearer_headers(token: str) -> dict:
    """
    Retorna un diccionario con el header Authorization Bearer.
    """
    return {"Authorization": f"Bearer {token}"}

def make_cookie_response(res: Response, token: str):
    """
    Crea una cookie de sesión segura en la respuesta dada, con el token proporcionado.
    El nombre de la cookie es "session_token"
    """
    res.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="Lax",
        secure=False,
        max_age=3600
    )

def flash_message(
        title: str, 
        description: str = '', 
        category: Literal['error', 'success', 'warning', 'info'] = 'error'
    ) -> None:
    """
    Flashea un mensaje con un formato específico para ser mostrado con SweetAlert en el frontend.
    El mensaje se formatea como un JSON con las claves "title" y "text", y se categoriza con la categoría dada (por defecto, 'error').
    """
    flash(json.dumps({
        "title": title,
        "text": description
    }), category)