from services.public.users import validate_admin_user
from constants import URL_ADMIN_RESERVATIONS
from utils.helpers import flash_message, make_request, default_flash
from services.public.reservations import (
    get_all_reservations
)

from flask import Blueprint, request, render_template, redirect, url_for

adm_bp_reservations = Blueprint("admin_reservations", __name__)

@adm_bp_reservations.route(rule="/", methods=["GET"])
def show():
    """Lista todas las reservaciones."""
    user, token = validate_admin_user()
    if not user:
        return token

    reservas, page, per_page, total_pages = get_all_reservations(token) # type: ignore

    cols = ['ID', 'Fecha', 'Estado', 'Email', 'Nro Mesa', 'Comensales']
    rows = [
    {
        "cells": [u["id"], u['reservation_datetime'], u["status_reservation"], u["user_email"], u["table_number"], u['amount']],
        "data": {
            "id": u["id"],
            "reservation_datetime": u['reservation_datetime'],
            "status_reservation": u["status_reservation"],
            "user_email": u["user_email"],
            "table_number": u["table_number"],
            "amount": u['amount']
        }
    }
    for u in reservas
    ]

    return render_template('admin/reservations.html',
        user=user,
        cols=cols,
        rows=rows,
        page_title="Administrar reservas",
        title="Reservas",
        plus_label="Agregar reserva",
        abm=True,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@adm_bp_reservations.route("/create", methods=["POST"])
def create_reservation():
    user, token = validate_admin_user()
    if not user:
        return token

    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    reservation_datetime = f"{fecha} {hora}:00:00" if fecha and hora else None

    payload = {
        'user_email': request.form.get('user_email'),
        'reservation_datetime': reservation_datetime,
        'table_id': request.form.get('table_id'),
        'people_amount': request.form.get('people_amount'),
        'status_reservation': request.form.get('status_reservation', 'Pending')
    }

    res = make_request(URL_ADMIN_RESERVATIONS, 'POST', data=payload, token=token) # type: ignore

    if res.status_code in (200, 201):
        flash_message('Reservación creada correctamente', category='success')
    else:
        default_flash(res)

    return redirect(url_for('admin_reservations.show'))


@adm_bp_reservations.route("/update/<int:reservation_id>", methods=["POST"])
def update(reservation_id):
    user, token = validate_admin_user()
    if not user:
        return token

    # Volvemos a armar el string combinado de fecha y hora para el backend
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    reservation_datetime = f"{fecha} {hora}:00:00" if fecha and hora else None

    payload = {
        'user_email': request.form.get('user_email'),
        'reservation_datetime': reservation_datetime,
        'table_id': request.form.get('table_id'),
        'people_amount': request.form.get('people_amount'),
        'status_reservation': request.form.get('status_reservation')
    }

    # Mandamos un PUT a la API con el ID de la reserva
    res = make_request(f"{URL_ADMIN_RESERVATIONS}/{reservation_id}", 'PUT', data=payload, token=token) # type: ignore

    if res.status_code == 200:
        flash_message('Reservación actualizada correctamente', category='success')
    else:
        default_flash(res)

    return redirect(url_for('admin_reservations.show'))