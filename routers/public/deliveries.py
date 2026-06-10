from services.public.deliveries import get_deliveries_user, get_delivery_user
from utils.helpers import flash_message, get_current_user

from flask import Blueprint, request, render_template, redirect, url_for

public_bp_deliveries = Blueprint('public_deliveries', __name__)

@public_bp_deliveries.route(rule="/", methods=["GET", 'POST'])
def show():
    token = request.cookies.get('session_token')
    if not token:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return redirect(url_for('public_auth.login'))
    
    headers = request.headers 
    if request.method == 'POST':
        pass

    deliveries = get_deliveries_user(token, headers)
    if deliveries is None:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return redirect(url_for('public_auth.login'))
    
    user = get_current_user()
    return render_template('public/delivery/deliveries.html', deliveries=deliveries, user=user)

@public_bp_deliveries.route("/<int:delivery_id>", methods=["GET", 'DELETE'])
def take_delivery(delivery_id: int):
    """Tomar un delivery y renderizarlo.\n
    """
    token = request.cookies.get('session_token')
    if not token:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return redirect(url_for('public_auth.login'))
    
    headers = request.headers
    if request.method == 'DELETE':
        pass
    
    delivery = get_delivery_user(token, delivery_id, headers=headers)
    if delivery is None:
        return redirect(url_for('public_auth.login'))
          
    user = get_current_user()
    return render_template('public/delivery/delivery.html', delivery=delivery, user=user)