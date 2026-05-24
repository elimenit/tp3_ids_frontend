from utils.request import make_request

from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

app.secret_key = 'una_clave_super_secreta_y_larga_para_desarrollo' 

# Blueprints
from routers.login import public_login_bp
app.register_blueprint(public_login_bp)

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    template = getattr(e, 'template', 'public/index.html')
    error_title = getattr(e, 'error_title', 'Error desconocido')
    description = str(e) or 'Se ha producido un error inesperado.'
    code = getattr(e, 'status_code', 500)
    return render_template(template, title=error_title, description=description), code

@app.route("/", methods=['GET'])
def main():
    user_id = request.args.get('user_id', type=int)
    user = None
    # Cargo inicialmente los modales
    if user_id:
        response = make_request(f"http://localhost:5000/public/users/{user_id}", "GET")
        if response.status_code == 200:
            user = response.json()

    # Busca mensajes de éxito en la URL
    success = request.args.get('success')
    title = request.args.get('title')
    description = request.args.get('description')

    return render_template('public/index.html', 
        user_id=user_id, 
        user=user, 
        modal=True,
        form_heading="Actualiza tu información",
        show_username=True,
        show_confirm_password=True,
        submit_label="Actualizar",
        form_action=url_for('public_login.update_user', user_id=user_id),
        success=success,
        title=title,
        description=description
        )

if __name__ == '__main__':
    app.run("localhost", 10000, debug=True)