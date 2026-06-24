from constants import URL_ADMIN_TABLES
from services.admin.helpers import get_all_admin
from utils.helpers import make_request

def get_all_tables(token: str) -> tuple[list[dict], int, int, int]:
    return get_all_admin(token, URL_ADMIN_TABLES)

def create_table(token: str, data: dict) -> tuple[bool, dict, int]:
    """Crear una nueva mesa"""
    res = make_request(URL_ADMIN_TABLES, 'POST', data=data, token=token)
    success = res.status_code in (200, 201)
    response = res.json() if res.text else {}
    return success, response, res.status_code

def update_table(token: str, table_id: int, data: dict) -> tuple[bool, dict, int]:
    """Actualizar una mesa existente"""
    res = make_request(f"{URL_ADMIN_TABLES}{table_id}", 'PUT', data=data, token=token)
    success = res.status_code == 200
    response = res.json() if res.text else {}
    return success, response, res.status_code

def delete_table(token: str, table_id: int) -> tuple[bool, dict, int]:
    """Eliminar/desactivar una mesa"""
    res = make_request(f"{URL_ADMIN_TABLES}{table_id}", 'DELETE', token=token)
    success = res.status_code == 200
    response = res.json() if res.text else {}
    return success, response, res.status_code
