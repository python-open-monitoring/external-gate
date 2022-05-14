from channel_box import ChannelBoxEndpoint
from simple_print import sprint


class WebsocketChannel(ChannelBoxEndpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expires = 1600
        self.encoding = "json"

    async def on_connect(self, websocket):
        channel_name = websocket.query_params.get("channel_name", "default")
        await self.channel_get_or_create(channel_name, websocket)
        sprint(f"WebsocketChannel :: channel created {channel_name}", s=1, p=1)
        await websocket.accept()
