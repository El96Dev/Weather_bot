import re
from datetime import time, datetime

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import api_requests
import crud
from keyboards import reply
from keyboards.notifications_time_keyboard import notifications_time_keyboard
from db_helper import db_helper
from utils import get_coordinates_from_city_button
from models import NotificationsType, NotificationsTime
from load_config import config


router = Router()


class SetNotificationsState(StatesGroup):
    set_notification_type = State()
    set_notifications_time = State()
    set_location_type = State()
    set_city = State()
    click_city_button = State()
    set_latituge = State()
    set_longitude = State()


@router.message(F.text == "Добавить оповещения")
async def add_notifications(message: types.Message, state: FSMContext):
    await message.answer(
        "Выберите тип оповещений:",
        reply_markup=reply.get_notifications_type_keyboard(),
    )
    await state.set_state(SetNotificationsState.set_notification_type)


@router.message(F.text, StateFilter(SetNotificationsState.set_notification_type))
async def set_notifications_type(message: types.Message, state: FSMContext):
    if message.text not in ["Текущая погода", "Прогноз погоды"]:
        await message.answer(
            "Данный формат уведомлений не поддерживается! Выберите один из предоставленных вариантов!",
            reply_markup=reply.get_notifications_type_keyboard(),
        )
    else:
        await message.answer(
            "Выберите время для получения уведомлений:",
            reply_markup=notifications_time_keyboard.get_notifications_time_keyboard(),
        )
        await state.update_data(notifications_type=message.text)
        await state.set_state(SetNotificationsState.set_notifications_time)


@router.message(F.text, StateFilter(SetNotificationsState.set_notifications_time))
async def set_notifications_time(message: types.Message, state: FSMContext):
    if notifications_time_keyboard.is_valid_button(message.text):
        if message.text == f"Утренние - {config.morning.get_notifications_time()}":
            await state.update_data(notifications_time=NotificationsTime.MORNING)
        elif message.text == f"Дневные - {config.day.get_notifications_time()}":
            await state.update_data(notifications_time=NotificationsTime.DAY)
        elif message.text == f"Вечерние - {config.evening.get_notifications_time()}":
            await state.update_data(notifications_time=NotificationsTime.EVENING)

        await state.set_state(SetNotificationsState.set_location_type)
        await message.answer("Выберите тип указания локации:", 
                            reply_markup=reply.get_location_type_keyboard())
    else:
        await message.answer("Выберите один из предоставленных вариантов!",
                             reply_markup=reply.get_notifications_time_keyboard())


@router.message(F.text == "Широта и долгота", StateFilter(SetNotificationsState.set_location_type))
async def choose_coordinates_location_type(message: types.Message, state: FSMContext):
    await message.answer("Укажите широту:", reply_markup=reply.get_remove_keyboard())
    await state.set_state(SetNotificationsState.set_latituge)


@router.message(F.text, StateFilter(SetNotificationsState.set_latituge))
async def set_latitude(message: types.Message, state: FSMContext):
    pattern = r"^[-+]?[0-9]*\.?[0-9]+$"
    if re.match(pattern, message.text):
        await message.answer("Укажите долготу:")
        await state.update_data(latitude=message.text)
        await state.set_state(SetNotificationsState.set_longitude)
    else:
        await message.answer("Широта должна быть числом!")


@router.message(F.text, StateFilter(SetNotificationsState.set_longitude))
async def set_longitude(message: types.Message, state: FSMContext):
    pattern = r"^[-+]?[0-9]*\.?[0-9]+$"
    if re.match(pattern, message.text):
        await state.update_data(longitude=message.text)
        data = await state.get_data()
        chat_id = message.chat.id
        notifications_type_str = data.get("notifications_type")
        notifications_time = data.get("notifications_time")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        city = api_requests.get_city_by_coordinates(latitude, longitude)
        notifications_type = NotificationsType.CURRENT if notifications_type_str == "Текущая погода" else NotificationsType.FORECAST

        try:
            session = db_helper.get_scoped_session()
            await crud.add_weather_notifictions(
                chat_id, notifications_type, city, latitude, longitude, notifications_time, session
            )
            notifications_time_str = notifications_time.strftime("%H:%M")
            await message.answer(
                f"Уведомления успешно добавлены! Они будут приходить ежедневно в {notifications_time_str}"
            )
        except crud.NotificationsLimitError as e:
            await message.answer(str(e))
        await state.clear()
    else:
        await message.answer("Широта должна быть числом!")


@router.message(F.text == "Название города", StateFilter(SetNotificationsState.set_location_type))
async def choose_city_location_type(message: types.Message, state: FSMContext):
    await message.answer(
        "Укажите название города с большой буквы:", reply_markup=reply.get_remove_keyboard()
    )
    await state.set_state(SetNotificationsState.set_city)


@router.message(F.text, StateFilter(SetNotificationsState.set_city))
async def set_city(message: types.Message, state: FSMContext):
    response = api_requests.get_city_coords(message.text)
    cities = response.json()
    cities_keyboard = reply.keybord_from_cities(cities)
    await state.update_data(cities=cities)
    await state.set_state(SetNotificationsState.click_city_button)
    await message.answer("Выберите необходимый город:", reply_markup=cities_keyboard)


@router.message(F.text, StateFilter(SetNotificationsState.click_city_button))
async def click_city_button(message: types.Message, state: FSMContext):
    button_city, button_country, button_state = message.text.split(", ")
    data = await state.get_data()
    cities = data.get("cities")
    coordinates = get_coordinates_from_city_button(
        cities, button_city, button_country, button_state
    )
    if coordinates is not None:
        chat_id = message.chat.id
        city = message.text
        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]
        notifications_type_str = data.get("notifications_type")
        notifications_time = data.get("notifications_time")
        notifications_type = NotificationsType.CURRENT if notifications_type_str == "Текущая погода" else NotificationsType.FORECAST

        try:
            session = db_helper.get_scoped_session()
            await crud.add_weather_notifictions(
                chat_id, notifications_type, city, latitude, longitude, notifications_time, session
            )
            notifications_time_str = config.get_notifications_time_value(notifications_time)
            await message.answer(
                f"Уведомления успешно добавлены! Они будут приходить ежедневно в {notifications_time_str}"
            )
        except crud.NotificationsLimitError as e:
            await message.answer(str(e))
        await state.clear()
    else:
        await message.answer("Данный город не был найден")
        await state.clear()
