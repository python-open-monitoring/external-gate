import asyncio

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount
from tortoise.contrib.starlette import register_tortoise

from channel.urls import routes as channel_routes
from consumer.subscriptions import consumer_subscriptions
from main.urls import routes as main_routes
from middleware import CustomHeaderMiddleware
from middleware import JWTAuthenticationBackend
from settings import DATABASE_URI_GATE
from settings import JWT_ALGORITHM
from settings import JWT_PREFIX
from settings import JWT_SECRET_KEY
from user.urls import routes as user_routes


middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
    Middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend(secret_key=str(JWT_SECRET_KEY), algorithm=JWT_ALGORITHM, prefix=JWT_PREFIX)),  # str(SECRET_KEY) is important
    Middleware(SessionMiddleware, secret_key=JWT_SECRET_KEY),
    Middleware(GZipMiddleware, minimum_size=1000),
    Middleware(CustomHeaderMiddleware),
]


routes = [
    Mount("/channel", routes=channel_routes),
    Mount("/user", routes=user_routes),
    Mount("/", routes=main_routes),
]


class AmqpHttpServer(Starlette):
    def __init__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.create_task(consumer_subscriptions())
        super().__init__(*args, **kwargs)


app = AmqpHttpServer(debug=True, routes=routes, middleware=middleware)


tortoise_models = [
    "user.models",
]

register_tortoise(app, db_url=DATABASE_URI_GATE, modules={"models": tortoise_models}, generate_schemas=True)
