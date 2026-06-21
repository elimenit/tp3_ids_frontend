from werkzeug import Response
from constants import URL_ADMIN_USERS
from services.admin.helpers import get_all_admin
from services.public.users import get_user
from utils.helpers import flash_message

from flask import request, redirect, url_for

def get_all_users(token: str) -> tuple[list[dict], int, int, int]:
    return get_all_admin(token, URL_ADMIN_USERS)

def validate_admin_user() -> tuple[dict, Response | str]:
    """
    Si todo sale bien, devuelve el usuario y el token. 
    En caso contrario, la variable usuario estará vacía y devolverá la Response de redirección
    """
    token = request.cookies.get('session_token')
    if not token:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return {}, redirect(url_for('auth.login')) # type: ignore

    user = get_user(token)
    if not user:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return {}, redirect(url_for('auth.login')) # type: ignore

    if user.get('category') != 'admin':
        flash_message("Acceso denegado", "No tienes permisos para acceder a esta página.", "error")
        return {}, redirect(url_for('main')) # type: ignore
    
    return user, token