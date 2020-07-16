import os


PG_URL = os.getenv('PG_URL', 'postgresql://postgres:radist@postgresql/postgres')
RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq/')
RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', 'messages')
KEY = os.getenv('KEY', '1234')