from utils.helpers import flash_message, extract_form
from services.public.users import get_current_user
from services.public.reservations import get_tables, create_reservation, get_reservation, cancel_by_token

from flask import Blueprint, request, render_template, redirect, url_for

public_bp_reservations = Blueprint('public_reservations', __name__)

@public_bp_reservations.route("/", methods=["GET"])
def new():
    user = get_current_user()

    if user is None:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return redirect(url_for('auth.login'))

    tables_data = get_tables()
    print(tables_data)
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

    if not token:
        flash_message(
            "No has iniciado sesión",
            "Por favor, inicie sesión para continuar.",
            "info"
        )
        return redirect(url_for('auth.login'))
    data = extract_form(["fecha", "hora", "table_id", "people_amount"])
    print(data)
    user = get_current_user()

    reserva_id, error = create_reservation(token, data)

    if reserva_id:
        return redirect(url_for(
            'public_reservations.confirmacion',
            id=reserva_id
        ))

    if error and error.get("tipo") == "mesa_no_disponible":
        flash_message(
            "Mesa no disponible",
            error.get("mensaje", ""),
            "warning"
        )
        mesas_libres = error.get("mesas_libres", [])
        return render_template(
            'public/reservations/new.html',
            tables=mesas_libres,
            fecha=data.get("fecha"),
            hora=data.get("hora"),
            user=user,
        )

    flash_message(
        "Error al reservar",
        error.get("mensaje", "Ocurrió un error inesperado.") if error else ""
    )
    return render_template(
        'public/reservations/new.html',
        tables=[],
        fecha=data.get("fecha"),
        hora=data.get("hora"),
        user=user,
    )


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
