import os
import asyncio
import json

from aio_pika import connect, IncomingMessage, ExchangeType
from models.models import *
from models.config import *


async def on_message(message: IncomingMessage):
    with message.process():
        data = json.loads(message.body.decode())
        msg = await Message.get(data['id'])
        await msg.update(status=MessageStatus.PROCESSED).apply()
        print('id={}, receiver={}, body={}'.format(
                data['id'],
                data['receiver'],
                data['body']
            )
        )


async def main():
    await db.set_bind(PG_URL)
    await db.gino.create_all()
    connection = await connect(RABBITMQ_URL)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        RABBITMQ_EXCHANGE,
        ExchangeType.DIRECT
    )
    queue = await channel.declare_queue(
        '{}-queue'.format(KEY),
        durable=True
    )
    await queue.bind(exchange, routing_key=KEY)
    await queue.consume(on_message)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()