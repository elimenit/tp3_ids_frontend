from flask import render_template

def get_login_template() -> str:
    return render_template("auth/login.html", login=True)

def get_signup_template() -> str:
    return render_template("auth/signup.html", signup=True)