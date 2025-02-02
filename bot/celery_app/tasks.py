from datetime import datetime, time, timedelta

import asyncio
from celery import shared_task, current_app
from celery.schedules import crontab

import crud
from utils import create_current_weather_report, create_weather_forecast
from api_requests import get_current_weather, get_weather_forecast
from main import bot
from models import NotificationsType, NotificationsTime
from db_helper import db_helper


def send_user_notification(chat_id: int, city: str, 
                           notifications_type: NotificationsType, 
                           latitude: str, longitude: str) -> None:
    if notifications_type == NotificationsType.CURRENT:
        response = get_current_weather(latitude, longitude)
        notification = create_current_weather_report(city, response)
    elif notifications_type == NotificationsType.FORECAST:
        response = get_weather_forecast(latitude, longitude)
        notification = create_weather_forecast(city, response)
        
    if len(notification) != 0:
        asyncio.run(bot.send_message(chat_id=chat_id, text=notification))


@shared_task
def send_notifications(notifications_time_str: str):
    try:
        notifications_time = NotificationsTime(notifications_time_str)
        session = db_helper.get_scoped_session()
        loop = asyncio.get_event_loop()
        notifications = loop.run_until_complete(crud.get_weather_notifications_by_time(session, notifications_time))
        for notification in notifications:
            send_user_notification(notification.chat_id, 
                                notification.city, 
                                notification.notifications_type, 
                                notification.latitude, 
                                notification.longitude)
    except ValueError:
        print(f"Invalid NotificationsTime string: {notifications_time_str}")