from services.public.users import get_user
from utils.helpers import make_request, flash_message

from flask import Blueprint, redirect, render_template, request, url_for

admin_bp_dashboards = Blueprint('admin_dashboards', __name__)

@admin_bp_dashboards.route('/')
def show():
    """
    print("Accediendo al dashboard")
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
    """
    return render_template('admin/dashboards.html', user=True)