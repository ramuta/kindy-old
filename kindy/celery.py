# background tasks
from __future__ import absolute_import
import os
from celery import Celery
from utils.deployment import is_local_env

if is_local_env():
    BROKER_URL = 'redis://127.0.0.1:6379/0'
else:
    BROKER_URL = os.environ['REDISCLOUD_URL']

app = Celery('kindy', broker=BROKER_URL)