from datetime import time
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, BigInteger, String, Float, Time, Enum as SqlAlchemyEnum

from .base import Base


class NotificationsType(Enum):
    CURRENT = "CURRENT"
    FORECAST = "FORECAST"


class NotificationsTime(Enum):
    MORNING = "MORNING"
    DAY = "DAY"
    EVENING = "EVENING"


class WeatherNotifications(Base):
    __tablename__ = "weather_notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    notifications_type: Mapped[NotificationsType] = mapped_column(
        SqlAlchemyEnum(NotificationsType)
    )
    city: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    notifications_time: Mapped[NotificationsTime] = mapped_column(
        SqlAlchemyEnum(NotificationsTime)
    )