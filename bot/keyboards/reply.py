from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


start_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Текущая погода"),
            KeyboardButton(text="Прогноз погоды"),
            KeyboardButton(text="Загрязнение воздуха"),
            KeyboardButton(text="Добавить оповещения"),
            KeyboardButton(text="Мои оповещения")
        ],
    ],
)

location_type_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Город"),
            KeyboardButton(text="Долгота и широта")
        ],
    ],
)

remove_keyboard = ReplyKeyboardRemove()