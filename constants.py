from dotenv import load_dotenv
import os

load_dotenv()

URL_API = os.getenv('URL_API')
URL_PUBLIC_USERS_BASE = f"{URL_API}/public/users/"
URL_PUBLIC_USERS_ME = f"{URL_API}/public/users/me"
URL_ADMIN_USERS = f"{URL_API}/admin/users/"
URL_LOGIN_PUBLIC = f"{URL_API}/public/login"

URL_RESERVATIONS        = f"{URL_API}/public/reservations/"
URL_RESERVATIONS_TABLES = f"{URL_API}/public/reservations/tables"
URL_RESERVATIONS_CANCEL = f"{URL_API}/public/reservations/cancelar"
URL_ADMIN_RESERVATIONS  = f"{URL_API}/admin/reservations"
URL_PUBLIC_MENU = f"{URL_API}/public/menus/"
URL_PUBLIC_EXTRA_SERVICES = f"{URL_API}/public/extra_services/"
URL_ADMIN_MENUS = f"{URL_API}/admin/menus/"
URL_ADMIN_EXTRA_SERVICES = f"{URL_API}/admin/extra_services/"
URL_DASHBOARDS = f"{URL_API}/admin/dashboards"
URL_PUBLIC_REVIEWS = f"{URL_API}/public/reviews/"
URL_PUBLIC_RESERVATIONS_ME = f"{URL_API}/public/reservations/me"
