from constants import URL_ADMIN_USERS
from services.admin.users import validate_admin_user, get_all_users
from utils.helpers import flash_message, make_request, default_flash

from flask import Blueprint, render_template, request, redirect, url_for

admin_bp_users = Blueprint('admin_users', __name__)

@admin_bp_users.route("/", methods=["GET"])
def show():
    user, token = validate_admin_user()
    if not user:
        return token

    users, page, per_page, total_pages = get_all_users(token) # type: ignore

    cols = ['ID', 'Nombre', 'Email', 'Categoria', 'Estado']
    rows = [
    {
        "cells": [u["id"], u["name"], u["email"], u["category"], u["status"]],
        "data": {
            "id": u["id"],
            "name": u["name"],
            "email": u["email"],
            "category": u["category"],
        }
    }
    for u in users
    ]

    return render_template('admin/abm/users.html',
        user=user,
        cols=cols,
        rows=rows,
        page_title="Administrar usuarios",
        title="Usuarios",
        plus_label="Agregar usuario",
        admin_user=True,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@admin_bp_users.route("/create", methods=["POST"])
def create_user():
    user, token = validate_admin_user()
    if not user:
        return token

    payload = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'category': request.form.get('category'),
    }

    res = make_request(URL_ADMIN_USERS, 'POST', data=payload, token=token) # type: ignore

    if res.status_code in (200, 201):
        flash_message('Usuario creado correctamente', category='success')
    else:
        default_flash(res)

    return redirect(url_for('admin_users.show'))


@admin_bp_users.route("/update/<int:user_id>", methods=["POST"])
def update_user(user_id):
    user, token = validate_admin_user()
    if not user:
        return token

    payload = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'category': request.form.get('category'),
    }

    password = request.form.get('password')
    if password:
        payload['password'] = password

    res = make_request(f"{URL_ADMIN_USERS}/{user_id}", 'PUT', data=payload, token=token) # type: ignore

    if res.status_code == 200:
        flash_message('Usuario actualizado correctamente', category='success')
    else:
        default_flash(res)

    return redirect(url_for('admin_users.show'))


@admin_bp_users.route("/toggle_status/<int:user_id>", methods=["POST"])
def toggle_status(user_id):
    user, token = validate_admin_user()
    if not user:
        return token

    res = make_request(f"{URL_ADMIN_USERS}/{user_id}", 'DELETE', token=token) # type: ignore

    if res.status_code == 200:
        flash_message('Estado actualizado correctamente', category='success')
    else:
        default_flash(res)

    return redirect(url_for('admin_users.show'))