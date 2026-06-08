from dotenv import load_dotenv
import os

load_dotenv()

URL_API = os.getenv('URL_API')
URL_PUBLIC_USERS_BASE = f"{URL_API}/public/users/"
URL_PUBLIC_USERS_ME = f"{URL_API}/public/users/me"
URL_LOGIN_PUBLIC = f"{URL_API}/public/login"
URL_DELIVERIES = f"{URL_API}/public/deliveries/"
URL_DASHBOARDS = f"{URL_API}/admin/dashboards"