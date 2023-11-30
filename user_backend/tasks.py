
from django.core.mail import send_mail

from main_info.celery import app


@app.task
def send_mail_task(*args):
    send_mail(*args)
