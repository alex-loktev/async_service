import os
import gino
import aio_pika
import logging

from aiohttp import web
from project.urls import urls
from project.models import db
from project.config import PG_URL, RABBITMQ_URL, RABBITMQ_EXCHANGE


logging.basicConfig(level=logging.INFO)


async def connect_rabbitmq(app):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        RABBITMQ_EXCHANGE,
        aio_pika.ExchangeType.DIRECT
    )
    app['exchange'] = exchange
    app['connection'] = connection


async def close_rabbitmq(app):
    connection = app['connection']
    await connection.close()


async def connect_db(app):
    engine = await gino.create_engine(PG_URL)
    db.bind = engine
    await db.gino.create_all()


async def close_db(app):
    await db.pop_bind().close()


def main():
    app = web.Application()
    app.add_routes(urls)
    app.on_startup.append(connect_db)
    app.on_startup.append(connect_rabbitmq)
    app.on_shutdown.append(close_db)
    app.on_shutdown.append(close_rabbitmq)
    web.run_app(app)


if __name__ == "__main__":
    logging.info('Server started')
    main()