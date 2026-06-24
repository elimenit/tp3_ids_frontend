# Constantes y helpers

from services.public.users import get_user
from services.public.reviews import get_reviews
# Librerias
from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request


app = Flask(__name__)

from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('FLASK_SECRET_KEY')
flask_port = os.getenv('FLASK_PORT')
flask_host = os.getenv('FLASK_HOST')
if not (secret_key or flask_port or flask_host):
    raise ValueError("Faltan variables de entorno en el archivo .env. Asegúrate de que FLASK_SECRET_KEY, FLASK_PORT y FLASK_HOST estén definidos.")
app.secret_key = secret_key

# Register Blueprints
from routers.auth import bp_auth
from routers.public.users import public_bp_users
from routers.public.reservations import public_bp_reservations
from routers.admin.reservations import adm_bp_reservations
from routers.public.menus import public_bp_menus
from routers.public.reviews import public_bp_reviews
from routers.public.extra_services import public_bp_extra_services
from routers.admin.menus import admin_bp_menus
from routers.admin.dashboards import admin_bp_dashboards
from routers.admin.users import admin_bp_users
from routers.admin.tables import admin_bp_tables
from routers.admin.extra_services import admin_bp_extra_services

app.register_blueprint(public_bp_users, url_prefix="/users")
app.register_blueprint(bp_auth, url_prefix="/auth")
app.register_blueprint(public_bp_reservations, url_prefix="/reservations")
app.register_blueprint(public_bp_extra_services, url_prefix="/extra_services")
app.register_blueprint(adm_bp_reservations, url_prefix="/admin/reservations")
app.register_blueprint(admin_bp_users, url_prefix="/admin/users")
app.register_blueprint(public_bp_menus, url_prefix="/menu")
app.register_blueprint(public_bp_reviews, url_prefix="/reviews")
app.register_blueprint(admin_bp_menus, url_prefix="/admin/menus")
app.register_blueprint(admin_bp_dashboards, url_prefix="/admin/dashboards")
app.register_blueprint(admin_bp_tables, url_prefix="/admin/tables")
app.register_blueprint(admin_bp_extra_services, url_prefix="/admin/extra_services")

# Errors
@app.errorhandler(404)
def not_found(error):
    return render_template('partials/error.html', error_name='Pagina No Encontrada', detail="Not found"), 404

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return render_template('partials/error.html', error_name='Hubo un error', detail=f"Error: {e}"), 500

@app.route("/", methods=['GET'])
def main():
    token = request.cookies.get('session_token')
    user = None

    if token:
        user = get_user(token)

    reviews = get_reviews(limit=4) or []
    return render_template('public/index.html', user=user, reviews=reviews)


if __name__ == '__main__':
    app.run(flask_host, int(flask_port)) # type: ignore