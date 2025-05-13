from celery import shared_task
from random import randint
import time


@shared_task
def test_task():

    time.sleep(randint(1,10))

    return True