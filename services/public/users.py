from constants import URL_PUBLIC_USERS_ME
from utils.helpers import flash_message, make_request

from flask import Response, request, redirect, url_for

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
        data = response.json()
        flash_message(
            data.get('message', 'Error desconocido.'),
            data.get('description', '')
        )
    return {}    

def validate_admin_user() -> tuple[dict, Response | str]:
    """
    Si todo sale bien, devuelve el usuario y el token. 
    En caso contrario, la variable usuario estará vacía y devolverá la Response de redirección
    """
    token = request.cookies.get('session_token')
    if not token:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return {}, redirect(url_for('public_auth.login')) # type: ignore

    user = get_user(token)
    if not user:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return {}, redirect(url_for('public_auth.login')) # type: ignore

    if user.get('category') != 'admin':
        flash_message("Acceso denegado", "No tienes permisos para acceder a esta página.", "error")
        return {}, redirect(url_for('main')) # type: ignore
    
    return user, token