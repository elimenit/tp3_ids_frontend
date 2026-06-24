from constants import URL_ADMIN_EXTRA_SERVICES
from services.admin.users import validate_admin_user
from services.public.extra_services import (
    get_all_extra_services,
    create_extra_service,
    update_extra_service,
    delete_extra_service
)
from utils.helpers import flash_message

from flask import Blueprint, render_template, request, redirect, url_for

admin_bp_extra_services = Blueprint('admin_extra_services', __name__)


@admin_bp_extra_services.route('/', methods=['GET'])
def show():
    user, token = validate_admin_user()
    if not user:
        return token

    services = get_all_extra_services(token)
    rows = [
        {
            'cells': [s['id'], s.get('nombre', ''), s.get('descripcion', ''), 'Si' if s.get('activo') else 'No'],
            'data': {
                'id': s['id'],
                'nombre': s.get('nombre', ''),
                'descripcion': s.get('descripcion', ''),
                'activo': 'true' if s.get('activo') else 'false'
            }
        }
        for s in services
    ]

    cols = ['ID', 'Nombre', 'Descripción', 'Activo']

    return render_template('admin/abm/extra_services.html',
        user=user,
        cols=cols,
        rows=rows,
        page_title='Administrar servicios extras',
        title='Servicios extras',
        plus_label='Agregar servicio',
        abm=True,
        page=1,
        per_page=len(rows),
        total_pages=1
    )


@admin_bp_extra_services.post('/create')
def create():
    user, token = validate_admin_user()
    if not user:
        return token

    data = request.form.to_dict()
    data['activo'] = request.form.get('activo') in ('on', 'true', '1')

    success, response, status = create_extra_service(token, data)
    if success:
        flash_message('Servicio creado correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo crear el servicio'),
            'error'
        )

    return redirect(url_for('admin_extra_services.show'))


@admin_bp_extra_services.post('/update/<int:service_id>')
def update(service_id: int):
    user, token = validate_admin_user()
    if not user:
        return token

    data = request.form.to_dict()
    data['activo'] = request.form.get('activo') in ('on', 'true', '1')

    success, response, status = update_extra_service(token, service_id, data)
    if success:
        flash_message('Servicio actualizado correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo actualizar el servicio'),
            'error'
        )

    return redirect(url_for('admin_extra_services.show'))


@admin_bp_extra_services.post('/toggle_status/<int:service_id>')
def remove(service_id: int):
    user, token = validate_admin_user()
    if not user:
        return token

    success, response, status = delete_extra_service(token, service_id)
    if success:
        flash_message('Servicio eliminado correctamente', category='success')
    else:
        flash_message(
            response.get('message', 'Error'),
            response.get('description', 'No se pudo eliminar el servicio'),
            'error'
        )

    return redirect(url_for('admin_extra_services.show'))
