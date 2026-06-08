# =============================================================================
# services/public/reservations.py  (FRONTEND)
# Se encarga de hablar con el backend usando make_request.
# El router llama a estas funciones y renderiza con los datos que devuelven.
# =============================================================================

from constants import (
    URL_RESERVATIONS,
    URL_RESERVATIONS_TABLES,
    URL_RESERVATIONS_CANCEL,
    URL_ADMIN_RESERVATIONS,
)
from utils.helpers import make_request, flash_message


def get_tables(token, fecha=None, hora=None):
    """
    Pide al backend la lista de mesas con su disponibilidad.
    Si llegan fecha y hora las manda como parámetros en la URL.
    Devuelve la lista de mesas o None si hubo error.
    """
    # Armamos los parámetros opcionales
    params = ""
    if fecha and hora:
        params = f"?fecha={fecha}&hora={hora}"

    url = f"{URL_RESERVATIONS_TABLES}{params}"

    response = make_request(url, "GET", token=token)

    if response.status_code == 200:
        return response.json()

    data = response.json()
    title = data.get('message', 'Error')
    description = data.get('description', '')
    flash_message(title, description)
    return None


def create_reservation(token, table_id, fecha, hora):
    """
    Le manda al backend los datos para crear una reservación.
    Devuelve (reserva_id, None) si salió bien.
    Devuelve (None, data) si hubo error, donde data puede tener mesas_libres.
    """
    data = {
        "table_id": table_id,
        "fecha":    fecha,
        "hora":     hora,
    }

    response = make_request(URL_RESERVATIONS, "POST", data=data, token=token)

    if response.status_code == 201:
        reserva_id = response.json().get("reserva_id")
        return reserva_id, None

    # Devolvemos el contenido del error para que el router lo maneje
    return None, response.json()


def get_reservation(token, reservation_id):
    """
    Pide al backend los datos de una reservación por ID.
    Devuelve la reservación o None si no existe.
    """
    url = f"{URL_RESERVATIONS}{reservation_id}"
    response = make_request(url, "GET", token=token)

    if response.status_code == 200:
        return response.json()

    return None


def cancel_by_token(qr_token):
    """
    Le pide al backend que cancele la reservación usando el token del QR.
    No necesita token JWT porque el cliente llega desde el email.
    Devuelve (True, mensaje) o (False, mensaje).
    """
    url = f"{URL_RESERVATIONS_CANCEL}?token={qr_token}"
    response = make_request(url, "GET")

    data = response.json()

    if response.status_code == 200:
        return True, data.get("mensaje", "Reservación cancelada")

    return False, data.get("error", "No se pudo cancelar")


def get_all_reservations(token):
    response = make_request(URL_ADMIN_RESERVATIONS, "GET", token=token)
    if response.status_code == 200:
        return response.json()
    return None


def update_reservation_status(token, reservation_id, new_status):
    """
    Le pide al backend que cambie el estado de una reservación.
    Uso: panel admin.
    """
    url    = f"{URL_ADMIN_RESERVATIONS}{reservation_id}/estado"
    data   = {"status_reservation": new_status}

    response = make_request(url, "POST", data=data, token=token)

    if response.status_code == 200:
        return True

    return False