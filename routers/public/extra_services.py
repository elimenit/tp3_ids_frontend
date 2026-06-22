from services.public.extra_services import get_public_extra_services
from utils.helpers import get_current_user
from flask import Blueprint, render_template

public_bp_extra_services = Blueprint('public_extra_services', __name__)

@public_bp_extra_services.route('/', methods=['GET'])
def show():
    user = get_current_user()
    services = get_public_extra_services()
    return render_template('public/extra_services.html', user=user, services=services)
