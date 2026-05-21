from flask import Blueprint, render_template

public_login_bp = Blueprint('public_login', __name__)

@public_login_bp.route("/signup")
def signup():
    return render_template("public/signup.html")

@public_login_bp.route("/login")
def login():
    return render_template("public/login.html")