from utils.helpers import make_request
from utils.admin import get_all_admin
from constants import URL_PUBLIC_MENU, URL_ADMIN_MENUS


def get_public_menu(category: str = None, name: str = None, limit: int = None, offset: int = None) -> list | None:
    params = []
    if category:
        params.append(f"category={category}")
    if name:
        params.append(f"name={name}")
    if limit is not None:
        params.append(f"_limit={limit}")
    if offset is not None:
        params.append(f"_offset={offset}")

    url = f"{URL_PUBLIC_MENU}?{'&'.join(params)}" if params else URL_PUBLIC_MENU
    response = make_request(url, "GET")
    if response.status_code == 200:
        return response.json()
    return None

def get_all_menus_abm(token: str):
    return get_all_admin(token, URL_ADMIN_MENUS)

def get_all_menus(token: str) -> tuple[list | None, int]:
    response = make_request(URL_ADMIN_MENUS, "GET", token=token)
    if response.status_code == 200:
        return response.json(), 200
    return None, response.status_code


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
