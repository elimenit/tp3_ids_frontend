from flask import request
from utils.helpers import make_request, default_flash

def build_pagination_url(url: str) -> tuple[str, int, int]:
    """Recibe una URL y le agrega los parámetros (buscados en la URL) que el back espera para la paginación. 
    
    Devuelve la URL creada, el número de página y la cantidad de registros por página"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    offset = (page - 1) * per_page
    return f"{url}?_limit={per_page}&_offset={offset}", page, per_page

