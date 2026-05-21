from flask import Flask, render_template

app = Flask(__name__)

# Blueprints
from routers.login import public_login_bp
app.register_blueprint(public_login_bp)

@app.route("/", methods=['GET'])
def main():
    return render_template('public/index.html')

if __name__ == '__main__':
    app.run("localhost", 10000, debug=True)