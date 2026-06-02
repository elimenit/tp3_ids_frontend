from utils.helpers import make_request, get_bearer_headers

from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request, url_for


app.secret_key = 'una_clave_super_secreta_y_larga_para_desarrollo' 
API_URL = "http://localhost:5000" 
URL_PUBLIC_USERS = f"{API_URL}/public/users/me"

# Register Blueprints
app.register_blueprint(public_bp_signup)
app.register_blueprint(public_bp_login)
app.register_blueprint(public_bp_deliveries, url_prefix="/deliveries")

# Errors
@app.errorhandler(Exception)
def server_down(error):
    return render_template('error.html', error_name='Hubo un error', detail=f"Error: {error}"), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_name='Pagina No Encontrada', detail="Not found"), 404

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    template = getattr(e, 'template', 'public/index.html')
    error_title = getattr(e, 'error_title', 'Error')
    description = str(e) or 'Se ha producido un error inesperado.'
    code = getattr(e, 'status_code', 500)
    return render_template(template, title=error_title, description=description), code

@app.route("/", methods=['GET'])
def main():
    # Obtener token de la cookie
    token = request.cookies.get('session_token')
    user = None
    
    # Busca mensajes de éxito en la URL
    success = request.args.get('success')
    title = request.args.get('title')
    description = request.args.get('description')

    # Si hay token, obtener datos del usuario usando el header Bearer
    if token:
        headers = get_bearer_headers(token)
        response = make_request(URL_PUBLIC_USERS, "GET", headers=headers)
        if response.status_code == 200:
            user = response.json()
        else:
            data = response.json()
            success = False
            title = data.get('message', '')
            description = data.get('description', '')
    
    return render_template('public/index.html', 
        user=user, 
        modal=True,
        form_heading="Actualiza tu información",
        show_username=True,
        show_confirm_password=True,
        submit_label="Actualizar",
        form_action=url_for('public_login.update_user'),
        success=success,
        title=title,
        description=description
        )


if __name__ == '__main__':
    app.run("localhost", 10000, debug=True)