from constants import URL_PUBLIC_REVIEWS, URL_PUBLIC_RESERVATIONS_ME
from utils.helpers import make_request


def get_reviews(limit: int = 10, offset: int = 0) -> list | None:
    url = f"{URL_PUBLIC_REVIEWS}?_limit={limit}&_offset={offset}"
    response = make_request(url, "GET")
    return response.json() if response.status_code == 200 else None


def get_my_reservations(token: str) -> tuple[list | None, int]:
    response = make_request(URL_PUBLIC_RESERVATIONS_ME, "GET", token=token)
    if response.status_code == 200:
        return response.json(), 200
    return None, response.status_code


def create_review(token: str, data: dict) -> tuple[bool, dict, int]:
    response = make_request(URL_PUBLIC_REVIEWS, "POST", data=data, token=token)
    return response.status_code == 201, response.json(), response.status_code


def update_review(token: str, review_id: int, data: dict) -> tuple[bool, dict, int]:
    url = f"{URL_PUBLIC_REVIEWS}{review_id}"
    response = make_request(url, "PUT", data=data, token=token)
    return response.status_code == 200, response.json(), response.status_code


def delete_review(token: str, review_id: int) -> tuple[bool, dict, int]:
    url = f"{URL_PUBLIC_REVIEWS}{review_id}"
    response = make_request(url, "DELETE", token=token)
    return response.status_code == 200, response.json(), response.status_code
