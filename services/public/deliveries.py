import requests
from constants import URL_API

URL_DELIVERIES = f"{URL_API}/public/deliveries"

def get_deliveries(user_id: int, headers: dict)-> dict | None:
    """Obtiene una Lista de deliveries.\n
    """
    if user_id < 1:
        return None
    
    response = requests.get(url=f"{URL_DELIVERIES}/{user_id}", headers=headers, timeout=10)
    if response.status_code == 200:
        deliveries = response.json()
        delis = []
        for delivery in deliveries:
            delivery["url"] = f"/deliveries/{user_id}/{delivery["id"]}"
            delis.append(delivery)
        print(delis)
        return delis
    return None

def get_delivery(user_id: int, delivery_id: int, headers: dict) -> dict | None:
    if user_id < 1 or delivery_id < 1:
        return None

    response = requests.get(url=f"{URL_DELIVERIES}/{str(user_id)}/{str(delivery_id)}", headers=headers, timeout=10)

    if response.status_code == 200:
        return response.json()
    return None

    
