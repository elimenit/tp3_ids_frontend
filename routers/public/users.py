from constants import URL_PUBLIC_USERS_ME
from utils.helpers import make_request, flash_message

from flask import request, redirect, url_for, Blueprint

public_bp_users = Blueprint('public_users', __name__)

@public_bp_users.route("/update", methods=['POST'])
def update_user():
    token = request.cookies.get('session_token')
    if not token:
        flash_message("Error de sesión", "No se ha iniciado sesión.")
        return redirect(url_for('main'))

    data_form = {
        "name": request.form.get('name'),
        "password": request.form.get('password')
    }

    if data_form["name"] and data_form["password"]:
        response = make_request(URL_PUBLIC_USERS_ME, "PUT", data=data_form, token=token)
        
    elif data_form["name"] or data_form["password"]:
        response = make_request(URL_PUBLIC_USERS_ME, "PATCH", data=data_form, token=token)

    if response.status_code in [204, 200]:
        flash_message("Perfil actualizado", "Tu perfil ha sido actualizado exitosamente.", 'success')
        return redirect(url_for('main'))
    else:
        data = response.json()
        flash_message(
            data.get('message', 'Error al actualizar.'),
            data.get('description', '')
        )
        return redirect(url_for('main'))

@public_bp_users.route("/delete", methods=['POST'])
def delete_user():
    token = request.cookies.get('session_token')
    if not token:
        flash_message("Error de sesión", "No se ha iniciado sesión.")
        return redirect(url_for('main'))

    response = make_request(URL_PUBLIC_USERS_ME, "DELETE", token=token)

    if response.status_code in [204, 200]:
        flash_message("Perfil eliminado", "Tu perfil ha sido eliminado exitosamente.", 'success')
        res = redirect(url_for('main'))
        res.delete_cookie("session_token")
        return res
    else:
        data = response.json()
        flash_message(
            data.get('message', 'Error al eliminar.'),
            data.get('description', '')
        )
        return redirect(url_for('main'))