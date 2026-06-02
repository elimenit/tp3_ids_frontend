from flask import redirect, render_template, url_for


def make_error(message: str, description: str = "Error desconocido", status_code: int = 500, template: str = "main"):
    """Crea una respuesta de error formateada lista para retornar.
    
    Devuelve una tupla (render_template(...), status_code) lista para usar como return directo.
    """
    return redirect(url_for('main', title=message, description=description))
