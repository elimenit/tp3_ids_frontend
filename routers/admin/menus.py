from services.public.menus import get_all_menus, create_menu, update_menu, delete_menu
from utils.helpers import flash_message, get_current_user

from flask import Blueprint, render_template, request, redirect, url_for, jsonify

admin_bp_menus = Blueprint('admin_menus', __name__)


@admin_bp_menus.route("/", methods=["GET"])
def show():
    token = request.cookies.get('session_token')
    if not token:
        flash_message("Acceso denegado", "Debes iniciar sesión para continuar.", "error")
        return redirect(url_for('public_auth.login'))
    user = get_current_user()
    return render_template('admin/menus.html',
        user=user,
        modal=True,
        form_heading="Actualiza tu información",
        show_username=True,
        show_confirm_password=True,
        submit_label="Actualizar",
        form_action=url_for('public_users.update_user'),
    )


@admin_bp_menus.route("/all", methods=["GET"])
def all_dishes():
    token = request.cookies.get('session_token')
    if not token:
        return jsonify({"mensaje": "No autorizado"}), 401

    menus, status = get_all_menus(token)
    if status == 401:
        return jsonify({"mensaje": "Sesión expirada"}), 401
    if status == 403:
        return jsonify({"mensaje": "Sin permisos de administrador"}), 403
    if menus is None:
        return jsonify({"mensaje": "No se pudo obtener el listado de platos"}), 502
    return jsonify(menus)


@admin_bp_menus.route("/create", methods=["POST"])
def create():
    token = request.cookies.get('session_token')
    if not token:
        return jsonify({"mensaje": "No autorizado"}), 401

    data = request.get_json()
    success, response, status = create_menu(token, data)
    if status in (401, 403):
        return jsonify(response), status
    return jsonify(response), 201 if success else status


@admin_bp_menus.route("/<int:menu_id>", methods=["PUT"])
def update(menu_id: int):
    token = request.cookies.get('session_token')
    if not token:
        return jsonify({"mensaje": "No autorizado"}), 401

    data = request.get_json()
    success, response, status = update_menu(token, menu_id, data)
    if status in (401, 403):
        return jsonify(response), status
    return jsonify(response), 200 if success else status


@admin_bp_menus.route("/<int:menu_id>", methods=["DELETE"])
def remove(menu_id: int):
    token = request.cookies.get('session_token')
    if not token:
        return jsonify({"mensaje": "No autorizado"}), 401

    success, response, status = delete_menu(token, menu_id)
    if status in (401, 403):
        return jsonify(response), status
    return jsonify(response), 200 if success else status
