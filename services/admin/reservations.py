from constants import URL_ADMIN_RESERVATIONS
from services.admin.helpers import get_all_admin
from utils.helpers import make_request

def get_all_reservations(token: str) -> tuple[list[dict], int, int, int]:
    return get_all_admin(token, URL_ADMIN_RESERVATIONS)

def update_reservation_status(token, reservation_id, new_status):
    """
    Le pide al backend que cambie el estado de una reservación.
    Uso: panel admin.
    """
    url = f"{URL_ADMIN_RESERVATIONS}{reservation_id}/estado"
    data = {"status_reservation": new_status}

    response = make_request(url, "POST", data=data, token=token)

    if response.status_code == 200:
        return True

    return False