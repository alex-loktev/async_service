from gino import Gino
from enum import Enum
from sqlalchemy.dialects.postgresql.json import JSONB


db = Gino()


class MessageStatus(Enum):
    RECEIVED = 'received'
    PROCESSED = 'processed'


class Message(db.Model):
    __tablename__ = 'Messages'

    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(JSONB(), nullable=False)
    status = db.Column(db.Enum(MessageStatus), nullable=False)