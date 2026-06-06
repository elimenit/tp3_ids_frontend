# Constantes y helpers
from constants import URL_PUBLIC_USERS_ME
from utils.helpers import make_request, flash_message
from routers.public.reservations import public_bp_reservations
# Librerias
from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request, url_for


app = Flask(__name__)

app.secret_key = 'una_clave_super_secreta_y_larga_para_desarrollo' 

# Register Blueprints
from routers.auth import public_bp_auth
from routers.public.users import public_bp_users
from routers.public.deliveries import public_bp_deliveries
from routers.public.reservations import public_bp_reservations

app.register_blueprint(public_bp_users, url_prefix="/users")
app.register_blueprint(public_bp_auth, url_prefix="/auth")
app.register_blueprint(public_bp_deliveries, url_prefix="/deliveries")
app.register_blueprint(public_bp_reservations, url_prefix="/reservations")


# Errors
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_name='Pagina No Encontrada', detail="Not found"), 404

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return render_template('error.html', error_name='Hubo un error', detail=f"Error: {e}"), 500

@app.route("/", methods=['GET'])
def main():
    token = request.cookies.get('session_token')
    user = None

    if token:
        response = make_request(URL_PUBLIC_USERS_ME, "GET", token=token)
        if response.status_code == 200:
            user = response.json()
        elif response.status_code != 401: # si es 401, simplemente no se ha iniciado sesión/expiró, no es un error
            data = response.json()
            flash_message(
                data.get('message', 'Error desconocido.'),
                data.get('description', '')
            )
    
    return render_template('public/index.html', 
        user=user, 
        modal=True,
        form_heading="Actualiza tu información",
        show_username=True,
        show_confirm_password=True,
        submit_label="Actualizar",
        form_action=url_for('public_users.update_user'),
        )


if __name__ == '__main__':
    app.run("localhost", 10000, debug=True)