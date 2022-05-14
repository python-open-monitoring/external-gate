import aiormq
from simple_print import sprint

from consumer import handlers
from settings import AMQP_URI


async def consumer_subscriptions():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()

    sprint(f"AMQP CONSUMER:     ready [yes]", c="green", s=1, p=1)

    monitor_stat__declared = await channel.queue_declare(f"monitoring:external__gate:monitor_stat", durable=True)
    await channel.basic_consume(monitor_stat__declared.queue, handlers.monitor_stat, no_ack=False)
