import requests
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint


public_bp_signup = Blueprint('public_signup', __name__)

@public_bp_signup.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # 1. Atrapas los datos del formulario de Jinja
        datos_formulario = {
            "name": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        
        url_backend = "http://localhost:5000/public/users"
        respuesta_api = requests.post(url_backend, json=datos_formulario)
        print(respuesta_api.content)
        if respuesta_api.status_code == 201:
            return redirect(url_for('main'))
        else:
            flash("Error al registrar el usuario en el sistema")
            
    return render_template("public/signup.html")