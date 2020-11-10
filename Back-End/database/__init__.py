import os
from mongoengine import (
    connect
)
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongomock://localhost')
connect('data_collection', host=MONGO_HOST)