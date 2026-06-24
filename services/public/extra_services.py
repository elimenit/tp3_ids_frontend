from constants import URL_ADMIN_EXTRA_SERVICES, URL_PUBLIC_EXTRA_SERVICES
from utils.helpers import make_request


def get_public_extra_services() -> list:
    response = make_request(URL_PUBLIC_EXTRA_SERVICES, "GET")
    if response.status_code == 200:
        return response.json()
    return []


def get_all_extra_services(token: str):
    response = make_request(URL_ADMIN_EXTRA_SERVICES, "GET", token=token)
    if response.status_code == 200:
        return response.json()
    return []


def create_extra_service(token: str, data: dict) -> tuple[bool, dict, int]:
    response = make_request(URL_ADMIN_EXTRA_SERVICES, "POST", data=data, token=token)
    return response.status_code == 201, response.json(), response.status_code


def update_extra_service(token: str, service_id: int, data: dict) -> tuple[bool, dict, int]:
    url = f"{URL_ADMIN_EXTRA_SERVICES}{service_id}"
    response = make_request(url, "PUT", data=data, token=token)
    return response.status_code == 200, response.json(), response.status_code


def delete_extra_service(token: str, service_id: int) -> tuple[bool, dict, int]:
    url = f"{URL_ADMIN_EXTRA_SERVICES}{service_id}"
    response = make_request(url, "DELETE", token=token)
    return response.status_code == 200, response.json(), response.status_code
