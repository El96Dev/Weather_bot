from datetime import time

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models import WeatherNotifications, NotificationsType, NotificationsTime


class NotificationsLimitError(Exception):
    pass


async def add_weather_notifictions(
    chat_id: int,
    type: NotificationsType,
    city: str,
    latitiude: float,
    longitude: float,
    notifications_time: NotificationsTime,
    session: AsyncSession,
) -> None:
    notifications_count = await count_user_weather_notifications(chat_id, type, session)
    print("Notifications count ", notifications_count)
    if notifications_count < 2:
        notifications = WeatherNotifications(
            chat_id=chat_id,
            notifications_type=type,
            city=city,
            latitude=latitiude,
            longitude=longitude,
            notifications_time=notifications_time,
        )
        session.add(notifications)
        await session.commit()
    else:
        raise NotificationsLimitError(
            "Превышен лимит уведомлений! (По 2 уведомления каждого типа)"
        )


async def get_weather_notifications(
    chat_id: int, session: AsyncSession
) -> list[WeatherNotifications]:
    stmt = select(WeatherNotifications).where(WeatherNotifications.chat_id == chat_id)
    result = await session.execute(stmt)
    notifications = result.scalars().all()
    return notifications


async def get_weather_notifications_by_time(
        session: AsyncSession, 
        notifications_time: NotificationsTime
    ) -> list[WeatherNotifications]:
    stmt = select(WeatherNotifications).where(WeatherNotifications.notifications_time==notifications_time)
    result = await session.execute(stmt)
    notifications = result.scalars().all()
    return notifications


async def count_user_weather_notifications(
    chat_id: int, notifications_type, session: AsyncSession
) -> int:
    stmt = select(func.count()).where(
        and_(
            WeatherNotifications.chat_id == chat_id,
            WeatherNotifications.notifications_type == notifications_type,
        )
    )
    result = await session.execute(stmt)
    notifications_count = result.scalars().one()
    return notifications_count


async def update_weather_notifications(
    chat_id: int, 
    notifications_id: int,
    updates: dict,
    session: AsyncSession,
) -> WeatherNotifications | None:
    stmt = select(WeatherNotifications).where(
        and_(
            WeatherNotifications.id == notifications_id,
            WeatherNotifications.chat_id == chat_id
        )
    )
    result = await session.execute(stmt)
    notifications = result.scalars().one_or_none()
    if notifications is not None:
        for key, value in updates.items():
            if hasattr(notifications, key):
                setattr(notifications, key, value)
        await session.commit()
        return notifications
    else:
        raise ValueError("Уведомления не были найдены!")


async def delete_weather_notifications(
    chat_id: int, notifications_id: int, session: AsyncSession
) -> None:
    stmt = select(WeatherNotifications).where(
        and_(
            WeatherNotifications.chat_id == chat_id,
            WeatherNotifications.id == notifications_id
        )
    )
    result = await session.execute(stmt)
    notifications = result.scalars().one_or_none()
    if notifications is not None:
        await session.delete(notifications)
        await session.commit()
    else:
        raise ValueError("Уведомления не были найдены!")
