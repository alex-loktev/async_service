import os
import asyncio
import json
import logging

from aio_pika import connect, IncomingMessage, ExchangeType
from models.models import *
from models.config import *


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(module)s - %(funcName)s: %(message)s')


async def on_message(message: IncomingMessage):
    with message.process():
        logging.info("Message processing")
        data = json.loads(message.body.decode())
        msg = await Message.get(data['id'])
        await msg.update(status=MessageStatus.PROCESSED).apply()
        logging.info("Message update")


async def main():
    logging.info("Worker started")
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
    logging.info("Connect to exchange and bind queue with key = {}".format(KEY))
    await queue.consume(on_message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()