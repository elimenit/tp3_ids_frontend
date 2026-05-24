from utils.request import make_request

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
            submit_label="Registrarse",
            back_img=True
        )

    data_form = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "password": request.form.get('password')
    }

    url_backend = "http://localhost:5000/public/users/register"
    response = make_request(url_backend, "POST", data_form)

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
            description=data.get('description', 'Por favor, intenta nuevamente.'),
            back_img=True
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
            back_img=True
        )
    
    url_backend = "http://localhost:5000/public/login/"
    response = make_request(url_backend, "POST", request.form)

    if response.status_code == 200:
        user_id = response.json().get('id')
        return redirect(url_for('main', user_id=user_id))
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
            back_img=True
        )

@public_login_bp.route("/update", methods=['POST'])
def update_user():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        e = Exception("No se ha iniciado sesión.")
        e.error_title = "Error de solicitud"
        e.status_code = 400
        raise e

    url_backend = f"http://localhost:5000/public/users/{user_id}"
    response = make_request(url_backend, "PUT", data=request.form)

    if response.status_code == 204:
        return redirect(url_for('main', 
            user_id=user_id, 
            success=True, 
            title="Perfil actualizado", 
            description="Tu perfil ha sido actualizado exitosamente."))
    else:
        data = response.json()
        e = Exception(data.get('description', 'Error desconocido.'))
        e.error_title = data.get('message', 'Error al actualizar.')
        e.status_code = response.status_code
        raise e


@public_login_bp.route("/logout", methods=['GET', 'POST'])
def logout():
    return redirect(url_for('main'))