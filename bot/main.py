import os
import logging

import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command

import api_requests
from new_notifications import router as new_notifications_router
from users_notifications import router as users_notifications_router
from keyboards import reply
from utils import (
    get_coordinates_from_city_button, 
    create_air_polution_report,
    create_current_weather_report,
    create_weather_forecast,
)


load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()
dp.include_router(new_notifications_router)
dp.include_router(users_notifications_router)

class SetLocation(StatesGroup):
    set_location_type = State()
    set_city = State()
    click_city_button = State()
    set_latitude = State()
    set_longitude = State()


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer("Добро пожаловать в Weather_bot!", reply_markup=reply.start_keyboard.as_markup())


@dp.message(F.text == "Текущая погода")
async def get_current_weather(message: types.Message, state: FSMContext):
    await message.answer("Выберите способ указания геолокации:", reply_markup=reply.location_type_keyboard.as_markup())
    await state.update_data(action="current_weather")
    await state.set_state(SetLocation.set_location_type)


@dp.message(F.text == "Название города", StateFilter(SetLocation.set_location_type))
async def choose_city_location_type(message: types.Message, state: FSMContext):
    await message.answer("Укажите название города с большой буквы:", reply_markup=reply.remove_keyboard)
    await state.set_state(SetLocation.set_city)


@dp.message(F.text, StateFilter(SetLocation.set_city))
async def set_city(message: types.Message, state: FSMContext):
    response = api_requests.get_city_coords(message.text)
    cities = response.json()
    cities_keyboard = reply.keybord_from_cities(cities)
    await state.update_data(cities=cities)
    await state.set_state(SetLocation.click_city_button)
    await message.answer("Выберите необходимый город:", reply_markup=cities_keyboard)


@dp.message(F.text, StateFilter(SetLocation.click_city_button))
async def click_city_button(message: types.Message, state: FSMContext):
    button_city, button_country, button_state = message.text.split(', ')
    data = await state.get_data()
    cities = data.get("cities")
    coordinates = get_coordinates_from_city_button(cities, button_city, button_country, button_state)
    if coordinates is not None:
        latitude = coordinates['latitude']
        longitude = coordinates['longitude']
        action = data.get("action")
        if action == "current_weather":
            response = api_requests.get_current_weather(latitude=latitude, longitude=longitude)
            report = create_current_weather_report(response.json())
            await message.answer(report, reply_markup=reply.remove_keyboard)
        elif action == "weather_forecast":
            response = api_requests.get_weather_forecast(latitude=latitude, longitude=longitude)
            report_list = create_weather_forecast(response.json())
            for report in report_list:
                await message.answer(report, reply_markup=reply.remove_keyboard)
        elif action == "air_polution":
            response = api_requests.get_air_polution(latitude=latitude, longitude=longitude)
            report = create_air_polution_report(response.json())
            await message.answer(report, reply_markup=reply.remove_keyboard)
    else:
        await message.answer("Данный город не был найден")
    await state.clear()


@dp.message(F.text == "Широта и долгота", StateFilter(SetLocation.set_location_type))
async def choose_coordinates_location_type(message: types.Message, state: FSMContext):
    await message.answer("Укажите широту:", reply_markup=reply.remove_keyboard)
    await state.set_state(SetLocation.set_latitude)


@dp.message(F.text, StateFilter(SetLocation.set_latitude))
async def set_latitude(message: types.Message, state: FSMContext):
    await state.update_data(latitude=message.text)
    await message.answer("Укажите долготу:")
    await state.set_state(SetLocation.set_longitude)


@dp.message(F.text, StateFilter(SetLocation.set_longitude))
async def set_longitude(message: types.Message, state: FSMContext):
    await state.update_data(longitude=message.text)
    data = await state.get_data()
    action = data.get("action")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    if action == "current_weather":
        response = api_requests.get_current_weather(latitude=latitude, longitude=longitude)
        report = create_current_weather_report(response.json())
        await message.answer(report, reply_markup=reply.remove_keyboard)
    elif action == "weather_forecast":
        response = api_requests.get_weather_forecast(latitude=latitude, longitude=longitude)
        report_list = create_weather_forecast(response.json())
        for report in report_list:
            await message.answer(report, reply_markup=reply.remove_keyboard)
    elif action == "air_polution":
        response = api_requests.get_air_polution(latitude=latitude, longitude=longitude)
        report = create_air_polution_report(response.json())
        await message.answer(report, reply_markup=reply.remove_keyboard)
    await state.clear()


@dp.message(F.text == "Прогноз погоды")
async def get_forecast_weather(message: types.Message, state: FSMContext):
    await message.answer("Выберите способ указания геолокации:", reply_markup=reply.location_type_keyboard.as_markup())
    await state.update_data(action="weather_forecast")
    await state.set_state(SetLocation.set_location_type)


@dp.message(F.text == "Загрязнение воздуха")
async def get_air_polution(message: types.Message, state: FSMContext):
    await message.answer("Выберите способ указания геолокации:", reply_markup=reply.location_type_keyboard.as_markup())
    await state.update_data(action="air_polution")
    await state.set_state(SetLocation.set_location_type)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
