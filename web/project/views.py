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
        request.app.logger.info('Got a message without body')
        return web.json_response({
                                    'success': False,
                                    'error': 'Message is empty'
                                 },
                                 status=400)
    request.app.logger.info('Got a message: {} with key = {}'.format(data, key))
    msg = await Message.create(body=data, status=MessageStatus.RECEIVED)
    data['id'] = msg.id
    exchange = request.app['exchange']
    msg_body = json.dumps(data).encode()
    message = aio_pika.Message(
        msg_body
    )
    await exchange.publish(message, routing_key=key)
    request.app.logger.info('Sent a message to exchange (message:{})'.format(data))
    return web.json_response({'success': True, 'id': msg.id}, status=200)


async def get_status_message(request):
    try:
        id = int(request.match_info['id'])
    except ValueError:
        request.app.logger.info('Got not valid id')
        return web.json_response({
                                  'success': False,
                                  'error': 'Message\'s id is not valid'},
                                 status=400
                                 )
    status = await Message.select('status').where(
    Message.id == id).gino.scalar()
    try:
        status = status.value
    except AttributeError:
        request.app.logger.info('Message is not found')
        return web.json_response({
                                  'success': False,
                                  'error': 'Message is not found'
                                  },
                                 status=404)
    request.app.logger.info('Get message with id = {}'.format(id))
    return web.json_response({
                                'success': True,
                                'message_status': status
                             },
                             status=200)