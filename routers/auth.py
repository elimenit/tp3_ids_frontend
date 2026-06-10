from constants import URL_PUBLIC_USERS_BASE, URL_LOGIN_PUBLIC
from utils.helpers import make_request, make_cookie_response, flash_message

from flask import Blueprint, render_template, request, redirect, url_for

public_bp_auth = Blueprint('public_auth', __name__)

@public_bp_auth.route("/signup", methods=['GET', 'POST'])
def signup():
    template = render_template("public/auth/signup.html",
            form_title="Registrarse",
            form_heading="¡Bienvenido!",
            form_action=url_for('public_auth.signup'),
            show_username=True,
            show_confirm_password=True,
            submit_label="Registrarse",
    )

    if request.method == 'GET':
        return template
    
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
        return template
    
@public_bp_auth.route("/login", methods=['GET', 'POST'])
def login():
    template = render_template("public/auth/login.html",
            form_title="Iniciar sesión",
            form_heading="¡Hola de nuevo!",
            form_action=url_for('public_auth.login'),
            show_username=False,
            show_confirm_password=False,
            submit_label="Iniciar sesión",
    )
    
    if request.method == 'GET':
        return template
    
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
        return template
    
@public_bp_auth.route("/logout", methods=['GET', 'POST'])
def logout():
    res = redirect(url_for('main'))
    res.delete_cookie("session_token")
    return res