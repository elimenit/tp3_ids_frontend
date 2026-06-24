# routers/menu.py
from services.public.menus import get_public_menu
from utils.helpers import flash_message
from services.public.users import get_current_user
from flask import Blueprint, render_template, request, redirect, url_for

public_bp_menus = Blueprint('public_menus', __name__)

@public_bp_menus.route("/", methods=["GET"])
def show():

    user = get_current_user()

    if user is None:
        flash_message("No has iniciado sesión", "Por favor, inicie sesión para continuar.", "info")
        return redirect(url_for('auth.login'))


    menu_data = get_public_menu()
  
    categories = sorted(list(set(item['category'] for item in menu_data if 'category' in item)))
    
    return render_template('public/menus/menu.html',
        user=user,
        menu_data=menu_data,
        categories=categories
    )