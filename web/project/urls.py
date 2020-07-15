from aiohttp import web
from .views import *


urls = [
    web.post('/webhooks/{key}', add_message),
    web.get('/messages/{id}', get_status_message),
]