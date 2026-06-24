# services/public/menus.py
from utils.helpers import make_request
from constants import URL_PUBLIC_MENU

def get_public_menu(category: str = "") -> list:
    """Retorna una lista de platos. Si falla, retorna lista vacía."""
    url = URL_PUBLIC_MENU
    if category and category != 'all':
        url += f"?category={category}"
        
    response = make_request(url, "GET")
    if response.status_code == 200:
        return response.json()
    return []