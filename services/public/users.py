from constants import URL_PUBLIC_USERS_ME
from utils.helpers import default_flash, make_request

from flask import request

def get_user(token: str) -> dict:
    """
    Obtiene la información del usuario actual usando el token JWT.
    Retorna un diccionario con la información del usuario o {} si no se pudo obtener.
    """
    response = make_request(URL_PUBLIC_USERS_ME, "GET", token=token)
    if response.status_code == 200:
        user = response.json()
        return user
    elif response.status_code != 401: # si es 401, simplemente no se ha iniciado sesión/expiró, no es un error
        default_flash(response)
    return {}    

def get_current_user() -> dict:
    """
    Obtiene el usuario autenticado a partir de la cookie de sesión.
    Retorna el dict del usuario o {} si no hay sesión válida.
    """
    token = request.cookies.get('session_token')
    if not token:
        return {}
    return get_user(token)

def is_employee() -> bool:
    user = get_current_user()
    if not user:
        return False
    return user.get('category') in ['admin', 'root', 'employee']

