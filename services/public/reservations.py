from constants import URL_RESERVATIONS, URL_PUBLIC_TABLES, URL_RESERVATIONS_CANCEL
from utils.helpers import default_flash, make_request

from flask import redirect, url_for

def get_tables():
    """
    Pide al backend la lista de mesas con su disponibilidad.
    Si llegan fecha y hora las manda como parámetros en la URL.
    Devuelve la lista de mesas o None si hubo error.
    """
    response = make_request(URL_PUBLIC_TABLES, "GET")

    if response.status_code == 200:
        return response.json()['data']

    default_flash(response)
    return None


def create_reservation(token, data):
    """
    Le manda al backend los datos para crear una reservación.
    Devuelve (reserva_id, None) si salió bien.
    Devuelve (None, data) si hubo error, donde data puede tener mesas_libres.
    """
    response = make_request(URL_RESERVATIONS, "POST", data=data, token=token)

    if response.status_code == 201:
        reserva_id = response.json().get("reserva_id")
        return reserva_id, None

    default_flash(response)
    return redirect(url_for('public_reservations.new'))

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