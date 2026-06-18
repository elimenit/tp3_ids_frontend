from services.public.users import validate_admin_user
from services.public.menus import get_all_menus_abm, create_menu, update_menu, delete_menu
from utils.helpers import flash_message

from flask import Blueprint, render_template, request, redirect, url_for

admin_bp_menus = Blueprint('admin_menus', __name__)


@admin_bp_menus.route("/", methods=["GET"])
def show():
    user, token = validate_admin_user()
    if not user:
        return token

    menus, page, per_page, total_pages = get_all_menus_abm(token) # type: ignore

    cols = ['Imagen', 'ID', 'Nombre', 'Categoría', 'Descripción', 'Precio', 'Disponible']
    rows = [
        {
            "cells": [u["image_url"], u["id"], u["name"], u["category"], u["description"], u["price"], u["available"]],
            "data": {
                "id": u["id"],
                "name": u["name"],
                "category": u["category"],
                "description": u["description"],
                "price": u["price"],
                "available": u["available"],
                "image_url": u["image_url"],
            }
        }
        for u in menus
    ]

    return render_template('admin/menus.html',
        user=user,
        cols=cols,
        rows=rows,
        page_title="Administrar menú",
        title="Menú",
        plus_label="Agregar producto",
        abm=True,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@admin_bp_menus.post("/create")
def create():
    user, token = validate_admin_user()
    if not user:
        return token

    data = request.form.to_dict()
    success, response, status = create_menu(token, data) # type: ignore

    if success:
        flash_message('Producto creado correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo crear el producto'),
            'error')

    return redirect(url_for('admin_menus.show'))


@admin_bp_menus.post("/update/<int:menu_id>")
def update(menu_id: int):
    user, token = validate_admin_user()
    if not user:
        return token

    data = request.form.to_dict()
    success, response, status = update_menu(token, menu_id, data) # type: ignore

    if success:
        flash_message('Producto actualizado correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo actualizar el producto'),
            'error')

    return redirect(url_for('admin_menus.show'))


@admin_bp_menus.post("/toggle_status/<int:menu_id>")
def remove(menu_id: int):
    user, token = validate_admin_user()
    if not user:
        return token

    success, response, status = delete_menu(token, menu_id) # type: ignore

    if success:
        flash_message('Estado actualizado correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo actualizar el producto'),
            'error')

    return redirect(url_for('admin_menus.show'))