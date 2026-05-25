from flask import Flask, render_template
# Blueprints
# Acceso al mundo
from routers.login import public_bp_login
from routers.signup import public_bp_signup
# Acceso a los Usuarios
from routers.public.deliveries import public_bp_deliveries

app = Flask(__name__, template_folder='templates', static_folder='static')


app.secret_key = 'una_clave_super_secreta_y_larga_para_desarrollo' 

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

@app.route("/", methods=['GET'])
def main():
    return render_template('public/index.html')


if __name__ == '__main__':
    app.run("localhost", 10000, debug=True)