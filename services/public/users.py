from constants import URL_PUBLIC_USERS_ME
from utils.helpers import flash_message, make_request


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