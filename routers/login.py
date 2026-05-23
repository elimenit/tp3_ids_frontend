import requests
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint

public_login_bp = Blueprint('public_login', __name__)

@public_login_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    title = None
    description = None

    if request.method == 'POST':
        data_form = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        
        url_backend = "http://localhost:5000/public/users/register"
        response = requests.post(url_backend, json=data_form)
        
        if response.status_code == 201:
            return redirect(url_for('main'))
        else:
            data = response.json()
            print(data)  # Para depuración
            message = data.get('mensaje', 'Error desconocido al registrarse.')
            description = data.get('description', 'Por favor, intenta nuevamente.')
            
    return render_template("public/signup.html", title=message, description=description)

@public_login_bp.route("/login")
def login():
    return render_template("public/login.html")