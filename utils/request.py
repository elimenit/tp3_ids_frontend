
import requests
from typing import Literal

def make_request(url: str, method: Literal["GET", "POST", "PUT", "DELETE"], data: dict = {}) -> requests.Response:
    if method == "POST":
        response = requests.post(url, json=data)
    elif method == "PUT":
        response = requests.put(url, json=data)
    elif method == "DELETE":
        response = requests.delete(url)
    else:
        response = requests.get(url)
    return response