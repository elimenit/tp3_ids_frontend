from constants import URL_DASHBOARDS
from services.public.users import get_user
from utils.helpers import make_request, flash_message

from flask import Blueprint, redirect, render_template, request, url_for
from datetime import datetime, timedelta

admin_bp_dashboards = Blueprint('admin_dashboards', __name__)

@admin_bp_dashboards.route('/')
@admin_bp_dashboards.route('/<string:area>')
def show(area: str = 'reservations'):
    token = request.cookies.get('session_token')
    if not token:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return redirect(url_for('public_auth.login'))

    user = get_user(token)
    if not user:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return redirect(url_for('public_auth.login'))

    if user.get('category') != 'admin':
        flash_message("Acceso denegado", "No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('main'))
    
    ftoday = datetime.now().strftime('%Y-%m-%d')
    inicio = request.args.get('inicio', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fin = request.args.get('fin', ftoday)
    dash_url = f"{URL_DASHBOARDS}/{area}?inicio={inicio}&fin={fin}"

    response = make_request(dash_url, 'GET', token=token)
    if response.status_code == 200:
        data: dict = response.json()
    else:
        data = response.json()
        flash_message(data.get('message', 'Error'), data.get('description', 'Se ha producido un error desconocido'))

    return render_template('admin/dashboards.html', user=user, area=area, data=data, inicio=inicio, fin=fin, hoy=ftoday)