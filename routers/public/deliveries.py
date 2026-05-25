from flask import Blueprint, request, render_template, flash, url_for, redirect
from services.public.deliveries import get_deliveries, get_delivery

public_bp_deliveries = Blueprint('public_deliveries', __name__)

@public_bp_deliveries.route(rule="/<int:user_id>", methods=["GET", 'POST'])
def show(user_id: int):
    headers = request.headers # Fijo
    print(user_id)
    if request.method == 'POST':
        pass

    deliveries = get_deliveries(user_id, headers)
    if deliveries is None:
        return render_template('login.html')
    
    return render_template('public/deliveries.html', deliveries=deliveries)

@public_bp_deliveries.route("/<int:user_id>/<int:delivery_id>", methods=["GET", 'DELETE'])
def take_delivery(user_id: int, delivery_id: int):
    """Tomar un delivery y renderizarlo.\n
    """
    headers = request.headers
    if request.method == 'DELETE':
        pass
    
    delivery = get_delivery(user_id, delivery_id, headers=headers)
    if delivery is None:
        return redirect('login')
          
    return render_template('public/delivery.html', delivery=delivery)