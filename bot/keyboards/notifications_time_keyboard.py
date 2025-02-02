from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from models import NotificationsTime
from load_config import config


class NotificationsTimeKeyboard:
    def __init__(self, config):
        self.config = config

    def get_notifications_time_keyboard(self):
        notifications_time_keyboard = ReplyKeyboardBuilder()
        notifications_time_keyboard.add(
            KeyboardButton(text=f"Утренние - {self.config.morning.get_notifications_time()}"),
            KeyboardButton(text=f"Дневные - {self.config.day.get_notifications_time()}"),
            KeyboardButton(text=f"Вечерние - {self.config.evening.get_notifications_time()}")
        )
        return notifications_time_keyboard.adjust(1, 1, 1).as_markup()
    
    def is_valid_button(self, button_text: str) -> bool:
        return button_text in [
            f"Утренние - {self.config.morning.get_notifications_time()}",
            f"Дневные - {self.config.day.get_notifications_time()}",
            f"Вечерние - {self.config.evening.get_notifications_time()}"
        ]


notifications_time_keyboard = NotificationsTimeKeyboard(config)