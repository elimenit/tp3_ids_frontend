from utils.helpers import make_request
from constants import URL_DELIVERIES


def get_deliveries(token: str, headers: dict) -> dict | None:
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

def get_delivery(token: str, delivery_id: int, headers: dict) -> dict | None:
    if delivery_id < 1:
        return None

    response = make_request(f"{URL_DELIVERIES}/{str(delivery_id)}", "GET", headers=headers, token=token)

    if response.status_code == 200:
        return response.json()
    return None

    
