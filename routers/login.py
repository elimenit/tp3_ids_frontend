from utils.request import post_request

import requests
from flask import render_template, request, redirect, url_for, Blueprint

public_login_bp = Blueprint('public_login', __name__)

@public_login_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("public/signup.html",
            form_title="Registrarse",
            form_heading="¡Bienvenido!",
            form_action=url_for('public_login.signup'),
            show_username=True,
            show_confirm_password=True,
            submit_label="Registrarse"
        )

    data_form = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "password": request.form.get('password')
    }

    url_backend = "http://localhost:5000/public/users/register"
    response = post_request(url_backend, data_form)

    if response.status_code == 201:
        user_id = response.json().get('id')
        return redirect(url_for('main', user_id=user_id))
    else:
        data = response.json()
        return render_template("public/signup.html",
            form_title="Registrarse",
            form_heading="¡Bienvenido!",
            form_action=url_for('public_login.signup'),
            show_username=True,
            show_confirm_password=True,
            submit_label="Registrarse",
            title=data.get('message', 'Error desconocido al registrarse.'),
            description=data.get('description', 'Por favor, intenta nuevamente.')
        )

@public_login_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("public/signup.html",
            form_title="Iniciar sesión",
            form_heading="¡Hola de nuevo!",
            form_action=url_for('public_login.login'),
            show_username=False,
            show_confirm_password=False,
            submit_label="Iniciar sesión"
        )
    
    url_backend = "http://localhost:5000/public/login/"
    response = post_request(url_backend, request.form)

    if response.status_code == 200:
        user_id = response.json().get('id')
        return redirect(url_for('main', user_id=user_id))
    else:
        data = response.json()
        return render_template("public/signup.html",
            form_title="Iniciar sesión",
            form_heading="¡Hola de nuevo!",
            form_action=url_for('public_login.login'),
            show_username=False,
            show_confirm_password=False,
            submit_label="Iniciar sesión",
            title=data.get('message', 'Error desconocido al iniciar sesión.'),
            description=data.get('description', 'Por favor, intenta nuevamente.')
        )
    
@public_login_bp.route("/logout", methods=['GET', 'POST'])
def logout():
    return redirect(url_for('main'))