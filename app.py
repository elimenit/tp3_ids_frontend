# Constantes y helpers
from services.public.users import get_user

# Librerias
from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request

app = Flask(__name__)

app.secret_key = 'una_clave_super_secreta_y_larga_para_desarrollo' 

# Register Blueprints
from routers.auth import public_bp_auth
from routers.public.users import public_bp_users
from routers.public.deliveries import public_bp_deliveries
from routers.public.menus import public_bp_menus
from routers.admin.menus import admin_bp_menus
from routers.admin.dashboards import admin_bp_dashboards

app.register_blueprint(public_bp_users, url_prefix="/users")
app.register_blueprint(public_bp_auth, url_prefix="/auth")
app.register_blueprint(public_bp_deliveries, url_prefix="/deliveries")
app.register_blueprint(public_bp_menus, url_prefix="/menu")
app.register_blueprint(admin_bp_menus, url_prefix="/admin/menus")
app.register_blueprint(admin_bp_dashboards, url_prefix="/admin/dashboards")

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
        user = get_user(token)

    return render_template('public/index.html', user=user)


if __name__ == '__main__':
    app.run("localhost", 10000, debug=True)