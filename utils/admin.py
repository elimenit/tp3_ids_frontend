from flask import request
from utils.helpers import make_request, default_flash

def build_pagination_url(url: str) -> tuple[str, int, int]:
    """Recibe una URL y le agrega los parámetros (buscados en la URL) que el back espera para la paginación. 
    
    Devuelve la URL creada, el número de página y la cantidad de registros por página"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    offset = (page - 1) * per_page
    return f"{url}?_limit={per_page}&_offset={offset}", page, per_page

def get_all_admin(token, url) -> tuple[list[dict], int, int, int]:
    """Hace una petición GET a la URL insertada, haciendo todo el proceso de paginación
    
    Devuelve los registros, el número de página, registros por página y cantidad de páginas"""
    new_url, page, per_page = build_pagination_url(url)

    response = make_request(new_url, "GET", token=token)
    if response.status_code == 200:
        data = response.json()
        records = data['data']
        count = data['count']
    else:
        default_flash(response)
        return [], 0, 0, 0
    
    total_pages: int  = (count + per_page - 1) // per_page
    return records, page, per_page, total_pages