import requests

from flask import render_template

def post_request(url: str, data: dict) -> requests.Response:
    try:
        response = requests.post(url, json=data)
    except requests.exceptions.ConnectionError:
        e = Exception("Por favor, intenta nuevamente más tarde.")
        e.error_title = "El servidor no está disponible"
        e.status_code = 503
        raise e
    return response