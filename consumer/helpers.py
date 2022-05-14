import asyncio
import datetime
import json
import uuid

import aiormq.types
from pydantic import ValidationError
from simple_print import sprint

from settings import AMQP_URI


class RpcClient:
    def __init__(self):
        self.connection = None  # type: aiormq.Connection
        self.channel = None  # type: aiormq.Channel
        self.callback_queue = ""
        self.futures = {}
        self.loop = asyncio.get_event_loop()

    async def connect(self):
        self.connection = await aiormq.connect(AMQP_URI)
        self.channel = await self.connection.channel()
        declare_ok = await self.channel.queue_declare(exclusive=True, auto_delete=True)

        await self.channel.basic_consume(declare_ok.queue, self.on_response)
        self.callback_queue = declare_ok.queue
        return self

    async def on_response(self, message: aiormq.types.DeliveredMessage):
        future = self.futures.pop(message.header.properties.correlation_id)
        future.set_result(message.body)

    async def call(self, outcoming_message_dict, routing_key):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        self.futures[correlation_id] = future
        outcoming_message_bytes = json.dumps(outcoming_message_dict).encode()
        await self.channel.basic_publish(
            outcoming_message_bytes,
            routing_key=routing_key,
            properties=aiormq.spec.Basic.Properties(
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=self.callback_queue,
            ),
        )
        body = await future
        incoming_message_dict = json.loads(body.decode())
        return incoming_message_dict


def validate_request_schema(request_schema, critical=False):
    def wrap(func):
        async def wrapped(message):
            now = datetime.datetime.now().time()

            sprint(f"{func.__name__} :: basic_ack [OK] :: {now}", c="green", s=1, p=1)

            if not critical:
                await message.channel.basic_ack(message.delivery.delivery_tag)  # для некритичных

            json_data = None
            error = None

            try:
                json_data = json.loads(message.body)
                validated_data = request_schema.validate(json_data).dict()
            except ValidationError as error_message:
                error = f"ERROR REQUEST, VALIDATION ERROR: body={message.body} error={error_message}"
            except Exception as error_message:
                error = f"ERROR REQUEST: body={message.body} error={error_message}"

            if not error:
                sprint(f"{func.__name__} :: Request {json_data}", c="yellow", s=1, p=1)
                try:
                    await func(validated_data)
                except Exception as error_message:
                    error = f"~ ERROR RESPONSE: body={message.body} error={error_message}"

            if error:
                sprint(error, c="red")
            else:
                sprint(f"{func.__name__} :: complete [OK]", c="green", s=1, p=1)

            if critical:
                await message.channel.basic_ack(message.delivery.delivery_tag)  # для критичных

        return wrapped

    return wrap
