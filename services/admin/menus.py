from constants import URL_ADMIN_MENUS
from services.admin.helpers import get_all_admin
from utils.helpers import make_request

def get_all_menus_abm(token: str):
    return get_all_admin(token, URL_ADMIN_MENUS)

def create_menu(token: str, data: dict) -> tuple[bool, dict, int]:
    response = make_request(URL_ADMIN_MENUS, "POST", data=data, token=token)
    print(response)
    return response.status_code == 201, response.json(), response.status_code

def update_menu(token: str, menu_id: int, data: dict) -> tuple[bool, dict, int]:
    url = f"{URL_ADMIN_MENUS}{menu_id}"
    response = make_request(url, "PUT", data=data, token=token)
    return response.status_code == 200, response.json(), response.status_code

def delete_menu(token: str, menu_id: int) -> tuple[bool, dict, int]:
    url = f"{URL_ADMIN_MENUS}{menu_id}"
    response = make_request(url, "DELETE", token=token)
    return response.status_code == 200, response.json(), response.status_code