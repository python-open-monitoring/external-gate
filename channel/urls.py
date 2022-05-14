from starlette.routing import WebSocketRoute

from .views import WebsocketChannel


routes = [
    WebSocketRoute("/ws", WebsocketChannel),
]
