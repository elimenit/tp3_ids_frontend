
import requests
from typing import Literal
from flask import render_template

def make_request(url: str, method: Literal["GET", "POST", "PUT", "DELETE"], data: dict = {}) -> requests.Response:
    try:
        if method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            response = requests.get(url)
    except requests.exceptions.ConnectionError:
        e = Exception("Por favor, intenta nuevamente más tarde.")
        e.error_title = "El servidor no está disponible"
        e.status_code = 503
        raise e
    return response