from datetime import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove 
from aiogram.utils.keyboard import ReplyKeyboardBuilder


start_keyboard = ReplyKeyboardBuilder()
start_keyboard.add(
    KeyboardButton(text="Текущая погода"),
    KeyboardButton(text="Прогноз погоды"),
    KeyboardButton(text="Загрязнение воздуха"),
    KeyboardButton(text="Добавить оповещения"),
    KeyboardButton(text="Мои оповещения")
)
start_keyboard.adjust(1, 1, 1, 1, 1)

location_type_keyboard = ReplyKeyboardBuilder()
location_type_keyboard.add(
    KeyboardButton(text="Название города"),
    KeyboardButton(text="Долгота и широта")
)
location_type_keyboard.adjust(1, 1)

notifications_type_keyboard = ReplyKeyboardBuilder()
notifications_type_keyboard.add(
    KeyboardButton(text="Текущая погода"),
    KeyboardButton(text="Прогноз погоды"),
)
notifications_type_keyboard.adjust(1, 1)

remove_keyboard = ReplyKeyboardRemove()

def keybord_from_cities(cities: list[dict]) -> ReplyKeyboardMarkup:
    cities_keyboard = ReplyKeyboardBuilder()
    for city in cities:
        cities_keyboard.add(KeyboardButton(text=f"{city['name']}, {city['country']}, {city['state']}"))
    cities_keyboard.adjust(1)
    return cities_keyboard.as_markup()

