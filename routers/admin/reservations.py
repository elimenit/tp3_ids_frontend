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
    return render_template('admin/reservations.html',
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
    
    print('\n',request.form.get('table_display'))
    
    payload = {
        'user_email': request.form.get('user_email'),
        'fecha': request.form.get('fecha'),
        'hora': request.form.get('hora'),
        'table_id': request.form.get('table_display'),
        'people_amount': request.form.get('people_amount'),
        'status_reservation': request.form.get('status_reservation')
    }
    print(payload)
    res = make_request(f"{URL_ADMIN_RESERVATIONS}/{reservation_id}", 'PUT', data=payload, token=token) # type: ignore

    if res.status_code == 204:
        flash_message('Reservación actualizada correctamente', category='success')
    else:
        default_flash(res)

    return redirect(url_for('admin_reservations.show'))