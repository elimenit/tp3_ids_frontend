# Login

## Formulario
Se creo un formulario dinámico con el cual, a través de parámetros específicos, puede ser reutilizado para actualización completa, parcial, registro e iniciado de sesión, es por eso que se observa repetidamente cosas como
```python
return render_template("public/signup.html",
    form_title="Registrarse",
    form_heading="¡Bienvenido!",
    form_action=url_for('public_login.signup'), 
    show_username=True,
    show_confirm_password=True,
    submit_label="Registrarse",
    modal=False # Esto es en caso de que queramos usar el formulario como modal en lugar de página dedicada 
)
```