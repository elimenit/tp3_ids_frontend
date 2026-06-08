from services.public.menus import get_public_menu
from utils.helpers import get_current_user

from flask import Blueprint, render_template, request, jsonify, url_for

public_bp_menus = Blueprint('public_menus', __name__)


@public_bp_menus.route("/", methods=["GET"])
def show():
    user = get_current_user()
    return render_template('public/menus/menu.html',
        user=user,
    )


@public_bp_menus.route("/dishes", methods=["GET"])
def dishes():
    """Proxy JSON hacia la API del backend. Lo consume menu.js vía fetch."""
    category = request.args.get('category')
    name = request.args.get('name')
    limit = request.args.get('_limit', type=int)
    offset = request.args.get('_offset', type=int)

    menus = get_public_menu(category=category, name=name, limit=limit, offset=offset)
    if menus is None:
        return jsonify({"mensaje": "No se pudo obtener el menú"}), 502
    return jsonify(menus)
