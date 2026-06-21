from services.admin.users import validate_admin_user
from services.admin.tables import get_all_tables, create_table, update_table, delete_table
from utils.helpers import flash_message

from flask import Blueprint, render_template, request, redirect, url_for

admin_bp_tables = Blueprint('admin_tables', __name__)


@admin_bp_tables.route("/", methods=["GET"])
def show():
    user, token = validate_admin_user()
    if not user:
        return token

    tables, page, per_page, total_pages = get_all_tables(token)  # type: ignore

    cols = ['ID', 'Capacidad', 'Estado']
    rows = [
        {
            "cells": [t["id"], t["capacity"], t["status"]],
            "data": {
                "id": t["id"],
                "capacity": t["capacity"]
            }
        }
        for t in tables
    ]

    return render_template('admin/abm/tables.html',
        user=user,
        cols=cols,
        rows=rows,
        page_title="Administrar mesas",
        title="Mesas",
        plus_label="Agregar mesa",
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@admin_bp_tables.post("/create")
def create():
    user, token = validate_admin_user()
    if not user:
        return token

    data = {
        'capacity': request.form.get('capacity'),
    }
    success, response, status = create_table(token, data)  # type: ignore

    if success:
        flash_message('Mesa creada correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo crear la mesa'),
            'error')

    return redirect(url_for('admin_tables.show'))


@admin_bp_tables.post("/update/<int:table_id>")
def update(table_id: int):
    user, token = validate_admin_user()
    if not user:
        return token

    data = {
        'capacity': request.form.get('capacity'),
    }
    success, response, status = update_table(token, table_id, data)  # type: ignore

    if success:
        flash_message('Mesa actualizada correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo actualizar la mesa'),
            'error')

    return redirect(url_for('admin_tables.show'))


@admin_bp_tables.post("/toggle_status/<int:table_id>")
def toggle_status(table_id: int):
    user, token = validate_admin_user()
    if not user:
        return token

    success, response, status = delete_table(token, table_id)  # type: ignore

    if success:
        flash_message('Estado actualizado correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo actualizar el estado'),
            'error')

    return redirect(url_for('admin_tables.show'))
