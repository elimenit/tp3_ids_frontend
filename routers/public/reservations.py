from flask import Blueprint, request, render_template, redirect, url_for
from utils.helpers import flash_message, get_current_user
from services.public.reservations import (
    get_tables,
    create_reservation,
    get_reservation,
    cancel_by_token,
    get_all_reservations,
    update_reservation_status,
)



public_bp_reservations = Blueprint('public_reservations', __name__)

@public_bp_reservations.route("/", methods=["GET"])
def new():
    token = request.cookies.get('session_token')
    tables_data = get_tables(token)
    user = get_current_user()

    return render_template('public/reservations/new.html',
                           tables=tables_data,
                           fecha="",
                           hora="",
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
        return redirect(url_for('public_auth.login'))

    fecha    = request.form.get("fecha")
    hora     = request.form.get("hora")
    table_id = request.form.get("table_id")
    user     = get_current_user()

    reserva_id, error = create_reservation(token, table_id, fecha, hora)

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
            fecha=fecha,
            hora=hora,
            user=user,
        )

    flash_message(
        "Error al reservar",
        error.get("mensaje", "Ocurrió un error inesperado.") if error else ""
    )
    return render_template(
        'public/reservations/new.html',
        tables=[],
        fecha=fecha,
        hora=hora,
        user=user,
    )


@public_bp_reservations.route("/<int:id>/confirmacion", methods=["GET"])
def confirmacion(id):
    """
    Pantalla de confirmación después de crear la reservación.
    GET /reservations/5/confirmacion
    """
    token = request.cookies.get('session_token')

    if not token:
        return redirect(url_for('public_auth.login'))

    reserva = get_reservation(token, id)

    if reserva is None:
        flash_message("Error", "Reservación no encontrada.")
        return redirect(url_for('public_reservations.new'))

    return render_template(
        'public/reservations/confirmacion.html',
        reserva=reserva,
        user=get_current_user(),
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


# =============================================================================
# RUTAS DEL ADMIN
# =============================================================================

@public_bp_reservations.route("/admin/", methods=["GET"])
def admin_index():
    """
    Listado de todas las reservaciones. Uso: panel admin.
    GET /reservations/admin/
    """
    token = request.cookies.get('session_token')

    if not token:
        flash_message(
            "No has iniciado sesión",
            "Por favor, inicie sesión para continuar.",
            "info"
        )
        return redirect(url_for('public_auth.login'))

    reservas = get_all_reservations(token)

    if reservas is None:
        flash_message("Error", "No se pudieron obtener las reservaciones.")
        reservas = []

    return render_template(
        'admin/reservations/index.html',
        reservas=reservas
    )


@public_bp_reservations.route("/admin/<int:id>", methods=["GET"])
def admin_detail(id):
    """
    Detalle de una reservación. Uso: panel admin.
    GET /reservations/admin/5
    """
    token = request.cookies.get('session_token')

    if not token:
        return redirect(url_for('public_auth.login'))

    reserva = get_reservation(token, id)

    if reserva is None:
        flash_message("Error", "Reservación no encontrada.")
        return redirect(url_for('public_reservations.admin_index'))

    return render_template(
        'admin/reservations/detail.html',
        reserva=reserva
    )


@public_bp_reservations.route("/admin/<int:id>/estado", methods=["POST"])
def admin_update_status(id):
    """
    Cambia el estado de una reservación. Uso: panel admin.
    POST /reservations/admin/5/estado
    """
    token = request.cookies.get('session_token')

    if not token:
        return redirect(url_for('public_auth.login'))

    nuevo_estado = request.form.get("status_reservation")

    ok = update_reservation_status(token, id, nuevo_estado)

    if ok:
        flash_message(
            "Estado actualizado",
            "El estado de la reservación fue actualizado.",
            "success"
        )
    else:
        flash_message("Error", "No se pudo actualizar el estado.")

    return redirect(url_for('public_reservations.admin_detail', id=id))