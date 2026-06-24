from utils.helpers import flash_message, extract_form, make_request, default_flash
from services.public.users import get_current_user, is_employee, get_user
from services.public.reservations import get_tables, create_reservation, get_reservation, cancel_by_token
from constants import URL_RESERVATIONS

from flask import Blueprint, request, render_template, redirect, url_for

public_bp_reservations = Blueprint('public_reservations', __name__)

@public_bp_reservations.route("/", methods=["GET"])
def new():
    user = get_current_user()

    if user is None:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return redirect(url_for('auth.login'))

    tables_data = get_tables()
    return render_template('public/reservations/new.html',
        tables=tables_data,
        fecha="",
        hora="",
        people_amount="",
        user=user)

@public_bp_reservations.route("/", methods=["POST"])
def create():
    """
    Recibe el formulario y crea la reservación en el backend.
    Maneja tres casos: éxito, mesa ocupada, error genérico.

    POST /reservations/
    """
    token = request.cookies.get('session_token')
    user = get_user(token)
    if not (token and user):
        flash_message(
            "No has iniciado sesión",
            "Por favor, inicie sesión para continuar.",
            "info"
        )
        return redirect(url_for('auth.login'))
    data = extract_form(["fecha", "hora", "table_id", "people_amount"])
    res = create_reservation(token, data)

    if isinstance(res, int):
        return redirect(url_for(
            'public_reservations.confirmacion',
            id=res
        ))
    return res

@public_bp_reservations.route("/<int:id>/confirmacion", methods=["GET"])
def confirmacion(id):
    """
    Pantalla de confirmación después de crear la reservación.
    GET /reservations/5/confirmacion
    """
    user = get_current_user()

    if user is None:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return redirect(url_for('auth.login'))

    token = request.cookies.get('session_token')
    reserva = get_reservation(token, id)

    if reserva is None:
        flash_message("Error", "Reservación no encontrada.")
        return redirect(url_for('public_reservations.new'))

    return render_template(
        'public/reservations/confirmacion.html',
        reserva=reserva,
        user=user,
    )


@public_bp_reservations.route("/cancelar", methods=["GET"])
def cancelar():
    """
    El cliente llega acá desde el link del email.
    No necesita estar logueado porque usa el token del QR.
    GET /reservations/cancelar?token=xK9mP2nQr7vL4wZj
    """
    qr_token = request.args.get("token")

    if not qr_token:
        flash_message("Error", "Token inválido.")
        return redirect(url_for('main'))

    ok, mensaje = cancel_by_token(qr_token)

    return render_template(
        'public/reservations/cancelacion.html',
        ok=ok,
        mensaje=mensaje,
        user=get_current_user(),
    )

@public_bp_reservations.route("/confirmar", methods=["GET"])
def confirmar():
    if not is_employee():
        flash_message('Error', 'No tienes los permisos para realizar esta acción. Por favor, contacta con un empleado', 'error')
        return redirect(url_for('main'))
    
    qr_token = request.args.get("token")
    if not qr_token:
        flash_message("Error", "Token inválido.")
        return redirect(url_for('main'))
    
    url = f"{URL_RESERVATIONS}confirm/{qr_token}"
    res = make_request(url, 'PATCH', {'status_reservation': 'Arrived'})
    if res.status_code == 200:
        reservation = res.json()
        flash_message('Reserva confirmada!',
            f'La reserva es en la mesa número {reservation.get('table_id')}, para la cantidad de {reservation.get('people_amount')} comensales.', 'success')
        return redirect(url_for('main'))
    else:
        default_flash(res)
        return redirect(url_for('main'))