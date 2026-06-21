from constants import URL_DASHBOARDS
from services.admin.users import validate_admin_user
from utils.helpers import make_request, flash_message

from flask import Blueprint, render_template, request
from datetime import datetime, timedelta

admin_bp_dashboards = Blueprint('admin_dashboards', __name__)

@admin_bp_dashboards.route('/')
@admin_bp_dashboards.route('/<string:area>')
def show(area: str = 'reservations'):
    user, token = validate_admin_user()
    if not user:
        return token
    
    ftoday = datetime.now().strftime('%Y-%m-%d')
    inicio = request.args.get('inicio', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fin = request.args.get('fin', ftoday)
    dash_url = f"{URL_DASHBOARDS}/{area}?inicio={inicio}&fin={fin}"

    response = make_request(dash_url, 'GET', token=token) # type: ignore
    if response.status_code == 200:
        data: dict = response.json()
    else:
        data = response.json()
        flash_message(data.get('message', 'Error'), data.get('description', 'Se ha producido un error desconocido'))

    return render_template('admin/dashboards.html', user=user, area=area, data=data, inicio=inicio, fin=fin, hoy=ftoday)