from starlette.routing import Route

from .views import change_password
from .views import refresh_token
from .views import reset_password
from .views import reset_password_confirm
from .views import user_login
from .views import user_register
from .views import user_register__default_1
from .views import user_register__default_2


routes = [
    Route("/register/default/1/Monitoring3f2SX5w2nJhMuWtU", endpoint=user_register__default_1, methods=["GET"], name="user_register__default_1"),
    Route("/register/default/2/Monitoring3f2SX5w2nJhMuWtU", endpoint=user_register__default_2, methods=["GET"], name="user_register__default_2"),
    Route("/register/", endpoint=user_register, methods=["POST", "OPTIONS"], name="user__register"),
    Route("/login/", endpoint=user_login, methods=["POST", "OPTIONS"], name="user__login"),
    Route("/refresh-token/", endpoint=refresh_token, methods=["POST", "OPTIONS"], name="user__refresh_token"),
    Route("/reset-password/", endpoint=reset_password, methods=["POST", "OPTIONS"], name="user__reset_password"),
    Route("/reset-password-confirm/", endpoint=reset_password_confirm, methods=["POST", "OPTIONS"], name="user__reset_password_confirm"),
    Route("/change-password/", endpoint=change_password, methods=["POST", "OPTIONS"], name="user__change_password"),
]
