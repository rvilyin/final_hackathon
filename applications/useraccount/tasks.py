from celery import Celery
from time import sleep
from celery import shared_task
from .models import Subscribe
import json
from datetime import datetime
import pytz
from .send_email import *

app = Celery('tasks', broker='redis://localhost:6379/0')

"""
date1 = datetime.strptime('2023-03-20', '%Y-%m-%d')
date2 = datetime.strptime('2023-03-10', '%Y-%m-%d')
delta = date1 - date2
print(delta.days)
"""


@shared_task
def check_data():
    data = Subscribe.objects.all()
    
    for d in data:
        local_tz = pytz.timezone('Europe/London')
        now = datetime.now(local_tz)
        total = now - d.created_at
        if total.days == 29:
            user = d.subscriber.username
            email = d.subscriber.email
            streamer = d.streamer.username
            send_notify_message(email, streamer, user)
        elif total.days == 30:
            d.delete()
