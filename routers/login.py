from utils.helpers import make_request, make_cookie_response, get_bearer_headers
from utils.error import make_error

from flask import render_template, request, redirect, url_for, Blueprint

public_login_bp = Blueprint('public_login', __name__)

API_URL = "http://localhost:5000" 
URL_PUBLIC_USERS_BASE = f"{API_URL}/public/users/" 
URL_PUBLIC_USERS_ME = f"{API_URL}/public/users/me" 
URL_LOGIN_PUBLIC = f"{API_URL}/public/login/"

@public_login_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    # Renderiza el formulario de registro
    if request.method == 'GET':
        return render_template("public/signup.html",
            form_title="Registrarse",
            form_heading="¡Bienvenido!",
            form_action=url_for('public_login.signup'),
            show_username=True,
            show_confirm_password=True,
            submit_label="Registrarse",
        )

    # Función principal para manejar el registro
    data_form = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "password": request.form.get('password')
    }

    response = make_request(URL_PUBLIC_USERS_BASE, "POST", data_form)

    if response.status_code == 201:
        token = response.json().get('token')
        
        res = redirect(url_for(
            'main', 
            success=True, 
            title="Registro exitoso", 
            description="Tu cuenta ha sido creada exitosamente."
        ))
        make_cookie_response(res, token) # type: ignore
        return res
    
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
            description=data.get('description', 'Por favor, intenta nuevamente.'),
        )

@public_login_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("public/login.html",
            form_title="Iniciar sesión",
            form_heading="¡Hola de nuevo!",
            form_action=url_for('public_login.login'),
            show_username=False,
            show_confirm_password=False,
            submit_label="Iniciar sesión",
        )
    
    response = make_request(URL_LOGIN_PUBLIC, "POST", request.form)

    if response.status_code == 200:
        token = response.json().get('token')
        
        res = redirect(url_for(
            'main', 
            success=True, 
            title="Inicio de sesión exitoso", 
            description="Tu cuenta ha sido iniciada exitosamente."
        ))
        make_cookie_response(res, token) # type: ignore
        return res
    else:
        data = response.json()
        return render_template("public/login.html",
            form_title="Iniciar sesión",
            form_heading="¡Hola de nuevo!",
            form_action=url_for('public_login.login'),
            show_username=False,
            show_confirm_password=False,
            submit_label="Iniciar sesión",
            title=data.get('message', 'Error desconocido al iniciar sesión.'),
            description=data.get('description', 'Por favor, intenta nuevamente.'),
        )

@public_login_bp.route("/update", methods=['POST'])
def update_user():
    token = request.cookies.get('session_token')
    if not token:
        return make_error("Error de solicitud", description="No se ha iniciado sesión.", status_code=401)

    data_form = {
        "name": request.form.get('name'),
        "password": request.form.get('password')
    }

    if data_form["name"] and data_form["password"]:
        response = make_request(URL_PUBLIC_USERS_ME, "PUT", data=data_form, token=token)
        
    elif data_form["name"] or data_form["password"]:
        response = make_request(URL_PUBLIC_USERS_ME, "PATCH", data=data_form, token=token)

    if response.status_code in [204, 200]:
        return redirect(url_for('main', 
            success=True, 
            title="Perfil actualizado", 
            description="Tu perfil ha sido actualizado exitosamente."))
    else:
        data = response.json()
        return make_error(
            data.get('message', 'Error al actualizar.'),
            description=data.get('description', 'Error desconocido.'),
            status_code=response.status_code,
        )

@public_login_bp.route("/delete", methods=['POST'])
def delete_user():
    token = request.cookies.get('session_token')
    if not token:
        return make_error("Error de solicitud", description="No se ha iniciado sesión.", status_code=401)

    response = make_request(URL_PUBLIC_USERS_ME, "DELETE", token=token)

    if response.status_code in [204, 200]:
        res = redirect(url_for('main', 
            success=True, 
            title="Perfil eliminado", 
            description="Tu perfil ha sido eliminado exitosamente."))
        res.delete_cookie("session_token")
        return res
    else:
        data = response.json()  
        return make_error(
            data.get('message', 'Error al eliminar.'),
            description=data.get('description', 'Error desconocido.'),
            status_code=response.status_code,
        )

@public_login_bp.route("/logout", methods=['GET', 'POST'])
def logout():
    res = redirect(url_for('main'))
    res.delete_cookie("session_token")
    return res