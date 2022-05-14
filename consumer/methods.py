from channel_box import channel_box


async def monitor_stat(data):
    """
    {
    "monitor_id": 3,
    "user_id": 1,
    "monitor_name": "ya.ru",
    "monitor_host": "ya.ru",
    "monitor_port": 443,
    "monitor_connection_establish": 1,
    "monitor_request_time": "12:00",
    "monitor_response_time": 4
    }
    """
    await channel_box.channel_send(f'user_id__{data["user_id"]}', data)
