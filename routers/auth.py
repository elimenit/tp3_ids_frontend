from constants import URL_PUBLIC_USERS_BASE, URL_LOGIN_PUBLIC
from utils.helpers import default_flash, make_request, make_cookie_response, flash_message, extract_form
from utils.templates import get_login_template, get_signup_template

from flask import Blueprint, request, redirect, url_for

bp_auth = Blueprint('auth', __name__)

@bp_auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return get_signup_template()
    
    data_form = extract_form(["name", "email", "password"])
    response = make_request(URL_PUBLIC_USERS_BASE, "POST", data_form)

    if response.status_code == 201:
        token = response.json().get('token')
        flash_message("Registro exitoso", "Tu cuenta ha sido creada exitosamente.", 'success')
        res = redirect(url_for('main'))
        make_cookie_response(res, token) # type: ignore
        return res
    else:
        default_flash(response)
        return get_signup_template()
    
@bp_auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return get_login_template()
    
    data_form = extract_form(["email", "password"])
    response = make_request(URL_LOGIN_PUBLIC, "POST", data_form)

    if response.status_code == 200:
        token = response.json().get('token')
        flash_message("Inicio de sesión exitoso", "Tu cuenta ha sido iniciada exitosamente.", 'success')
        res = redirect(url_for('main'))
        make_cookie_response(res, token) # type: ignore
        return res
    else:
        default_flash(response)
        return get_login_template()
    
@bp_auth.route("/logout", methods=['GET', 'POST'])
def logout():
    res = redirect(url_for('main'))
    res.delete_cookie("session_token")
    return res