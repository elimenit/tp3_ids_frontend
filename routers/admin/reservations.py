"""Rutas admin de reservaciones para el frontend.\n
"""
from flask import Blueprint, request, render_template, redirect, url_for
from utils.helpers import flash_message
from services.public.reservations import (
    get_all_reservations,
    get_reservation,
    update_reservation_status,
)
from services.public.users import get_user

adm_bp_reservations = Blueprint("admin_reservations", __name__)


@adm_bp_reservations.route(rule="/", methods=["GET"])
def show():
    """Lista todas las reservaciones.\n
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

    user = get_user(token)

    return render_template(
        'admin/reservations/index.html',
        reservas=reservas,
        user=user
    )


@adm_bp_reservations.route(rule="/<int:id>", methods=["GET"])
def detail(id: int):
    """Detalle de una reservacion.\n
    """
    token = request.cookies.get('session_token')

    if not token:
        return redirect(url_for('public_auth.login'))

    reserva = get_reservation(token, id)

    if reserva is None:
        flash_message("Error", "Reservación no encontrada.")
        return redirect(url_for('admin_reservations.show'))

    user = get_user(token)

    return render_template(
        'admin/reservations/detail.html',
        reserva=reserva,
        user=user
    )


@adm_bp_reservations.route(rule="/<int:id>/estado", methods=["POST"])
def update_status(id: int):
    """Cambia el estado de una reservacion.\n
    """
    token = request.cookies.get('session_token')

    if not token:
        return redirect(url_for('public_auth.login'))

    nuevo_estado = request.form.get("status_reservation")

    ok = update_reservation_status(token, id, nuevo_estado)

    if ok:
        flash_message(
            "Estado actualizado",
            "El estado fue actualizado correctamente.",
            "success"
        )
    else:
        flash_message("Error", "No se pudo actualizar el estado.")

    return redirect(url_for('admin_reservations.detail', id=id))