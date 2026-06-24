from services.admin.users import validate_admin_user
from constants import URL_ADMIN_RESERVATIONS
from utils.helpers import extract_form, flash_message, make_request, default_flash
from services.admin.reservations import get_all_reservations

from flask import Blueprint, request, render_template, redirect, url_for

adm_bp_reservations = Blueprint("admin_reservations", __name__)

@adm_bp_reservations.route(rule="/", methods=["GET"])
def show():
    """Lista todas las reservaciones."""
    user, token = validate_admin_user()
    if not user:
        return token
    reservas, page, per_page, total_pages = get_all_reservations(token) # type: ignore
    cols = ['ID', 'Fecha', 'Hora', 'Estado', 'Email', 'Nro Mesa', 'Comensales']
    rows = [
    {
        "cells": [u["id"], u['fecha'], u['hora'], u["status_reservation"], u["user_email"], u["table_number"], u['people_amount']],
        "data": {
            "id": u["id"],
            "fecha": u['fecha'],
            "hora": u['hora'],
            "status_reservation": u["status_reservation"],
            "user_email": u["user_email"],
            "table_number": u["table_number"],
            "people_amount": u['people_amount']
        }
    }
    for u in reservas
    ]
    return render_template('admin/abm/reservations.html',
        user=user,
        cols=cols,
        rows=rows,
        page_title="Administrar reservas",
        title="Reservas",
        abm=True,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@adm_bp_reservations.route("/update/<int:reservation_id>", methods=["POST"])
def update(reservation_id):
    user, token = validate_admin_user()
    if not user:
        return token
    
    payload = extract_form(["user_email", "fecha", "hora", "table_display", "people_amount", "status_reservation"]) 
    payload['table_id'] = payload.pop('table_display') # El backend espera 'table_id', pero el form tiene 'table_display' para mostrar el número de mesa
    res = make_request(f"{URL_ADMIN_RESERVATIONS}/{reservation_id}", 'PUT', data=payload, token=token) # type: ignore

    if res.status_code == 204:
        flash_message('Reservación actualizada correctamente', category='success')
    else:
        default_flash(res)

    return redirect(url_for('admin_reservations.show'))