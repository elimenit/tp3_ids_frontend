from flask import Flask, render_template

app = Flask(__name__)

app.secret_key = 'una_clave_super_secreta_y_larga_para_desarrollo' 

# Blueprints
from routers.login import public_login_bp
app.register_blueprint(public_login_bp)

@app.route("/", methods=['GET'])
def main():
    return render_template('public/index.html')

if __name__ == '__main__':
    app.run("localhost", 10000, debug=True)