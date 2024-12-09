from datetime import time
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, Time, Enum as SqlAlchemyEnum

from base import Base


class NotificationsType(Enum):
    CURRENT = 'CURRENT'
    FORECAST = 'FORECAST'


class WeatherNotifications(Base):
    __tablename__ = "weather_notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    report_type: Mapped[NotificationsType] = mapped_column(SqlAlchemyEnum(NotificationsType))
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    report_time: Mapped[time] = mapped_column(Time(timezone=True), nullable=False)