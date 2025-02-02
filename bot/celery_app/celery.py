import os
from datetime import timedelta

from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

from models import NotificationsTime
from load_config import config
from .tasks import send_notifications


load_dotenv()

celery_app = Celery('celery_app', broker=os.getenv('CELERY_BROKER_URL'), backend=os.getenv('CELERY_BACKEND'))
celery_app.conf.timezone = 'Europe/Moscow'
celery_app.conf.enable_utc = False
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.autodiscover_tasks = True

celery_app.conf.beat_schedule = {
    'send_morning_notifications': {
        'task': 'celery_app.tasks.send_notifications', 
        'schedule': crontab(hour=config.morning.get_hour(), 
                            minute=config.morning.get_minute()),  
        'args': [NotificationsTime.MORNING.value],
    },
    'send_day_notifications': {
        'task': 'celery_app.tasks.send_notifications', 
        'schedule': crontab(hour=config.day.get_hour(), 
                            minute=config.day.get_minute()),  
        'args': [NotificationsTime.DAY.value],
    },
    'send_evening_notifications': {
        'task': 'celery_app.tasks.send_notifications', 
        'schedule': crontab(hour=config.evening.get_hour(), 
                            minute=config.evening.get_minute()),  
        'args': [NotificationsTime.EVENING.value],
    },
}