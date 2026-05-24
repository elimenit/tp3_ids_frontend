from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request

app = Flask(__name__)

app.secret_key = 'una_clave_super_secreta_y_larga_para_desarrollo' 

# Blueprints
from routers.login import public_login_bp
app.register_blueprint(public_login_bp)

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    template = getattr(e, 'template', 'public/index.html')
    error_title = getattr(e, 'error_title', 'Error desconocido')
    description = str(e) or 'Se ha producido un error inesperado.'
    code = getattr(e, 'status_code', 500)
    return render_template(template, title=error_title, description=description), code

@app.route("/", methods=['GET'])
def main():
    user_id = request.args.get('user_id') # Para el logging
    return render_template('public/index.html', user_id=user_id)

if __name__ == '__main__':
    app.run("localhost", 10000, debug=True)