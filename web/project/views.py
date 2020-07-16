import json
import aio_pika
import os

from aiohttp import web
from .models import *
from .config import RABBITMQ_URL, RABBITMQ_EXCHANGE


async def add_message(request):
    key = request.match_info['key']
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        return web.Response(status=400, text="message is empty")
    msg = await Message.create(body=data, status=MessageStatus.RECEIVED)
    data['id'] = msg.id
    exchange = request.app['exchange']
    msg_body = json.dumps(data).encode()
    message = aio_pika.Message(
        msg_body
    )
    resp = {'status':'success', 'id':msg.id}
    await exchange.publish(message, routing_key=key)
    return web.Response(status=200, text=json.dumps(resp))


async def get_status_message(request):
    try:
        id = int(request.match_info['id'])
    except ValueError:
        return web.Response(status=404, text="Not found")
    status = await Message.select('status').where(
    Message.id == id).gino.scalar()
    try:
        resp = {'status': status.value}
    except AttributeError:
        return web.Response(status=404, text="Not found")
    return web.Response(status=200, text=json.dumps(resp))