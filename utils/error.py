from flask import render_template


def make_error(message: str, *, description: str = "Error desconocido", status_code: int = 500, template: str = "public/index.html"):
    """Crea una respuesta de error formateada lista para retornar.
    
    Devuelve una tupla (render_template(...), status_code) lista para usar como return directo.
    """
    return render_template(template, title=message, description=description), status_code
