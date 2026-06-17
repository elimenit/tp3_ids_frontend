from utils.helpers import make_request, requests
from constants import URL_DELIVERIES

# Deliveries USER
def get_deliveries_user(token: str, headers: dict) -> dict | None:
    """Obtiene una Lista de deliveries.\n
    """
    response = make_request(URL_DELIVERIES, "GET", headers=headers, token=token)
    if response.status_code == 200:
        deliveries = response.json()
        delis = []
        for delivery in deliveries:
            delivery["url"] = f"/deliveries/{delivery["id"]}"
            delis.append(delivery)
        print(delis)
        return delis
    return None

def get_delivery_user(token: str, delivery_id: int, headers: dict) -> None:
    if delivery_id < 1:
        return None

    response = make_request(f"{URL_DELIVERIES}/{str(delivery_id)}", "GET", headers=headers, token=token)

    if response.status_code == 200:
        return response.json()
    return None

def create_delivery(token: str, menus: list[str], headers: dict)-> None:
    if not token or not menus:
        return None

    response = requests.post(url=f"{URL_DELIVERIES}", json=menus ,headers=headers)

def delete_delivery_user(token: str, delivery_id, headers: dict)-> None:
    if delivery_id < 1 :
        return None
    response = make_request(f"{URL_DELIVERIES}/{str(delivery_id)}", "DELETE", headers=headers, token=token)
    if response.status_code == 200:
        return response.json()
    return None