import os


PG_URL = os.getenv('PG_URL', 'postgresql://postgres:radist@localhost/postgres')
RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost/')
RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', 'messages')
