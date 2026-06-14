from constants import URL_PUBLIC_USERS_BASE, URL_LOGIN_PUBLIC
from utils.helpers import make_request, make_cookie_response, flash_message
from utils.templates import get_login_template, get_signup_template

from flask import Blueprint, request, redirect, url_for

public_bp_auth = Blueprint('public_auth', __name__)

@public_bp_auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return get_signup_template()
    
    data_form = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "password": request.form.get('password')
    }

    response = make_request(URL_PUBLIC_USERS_BASE, "POST", data_form)

    if response.status_code == 201:
        token = response.json().get('token')
        flash_message("Registro exitoso", "Tu cuenta ha sido creada exitosamente.", 'success')
        res = redirect(url_for('main'))
        make_cookie_response(res, token) # type: ignore
        return res
    else:
        data = response.json()
        flash_message(
            data.get('message', 'Error desconocido al registrarse.'),
            data.get('description', '')
        )
        return get_signup_template()
    
@public_bp_auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return get_login_template()
    
    response = make_request(URL_LOGIN_PUBLIC, "POST", request.form)

    if response.status_code == 200:
        token = response.json().get('token')
        flash_message("Inicio de sesión exitoso", "Tu cuenta ha sido iniciada exitosamente.", 'success')
        res = redirect(url_for('main'))
        make_cookie_response(res, token) # type: ignore
        return res
    else:
        data = response.json()
        flash_message(
            data.get('message', 'Error desconocido al iniciar sesión.'),
            data.get('description', '')
        )
        return get_login_template()
    
@public_bp_auth.route("/logout", methods=['GET', 'POST'])
def logout():
    res = redirect(url_for('main'))
    res.delete_cookie("session_token")
    return res