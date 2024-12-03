import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command

from keyboards import reply


load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()

class SetReportState(StatesGroup):
    set_notification_type = State()
    set_time = State()
    set_location_type = State()
    set_city = State()
    set_latituge = State()
    set_longitude = State()


class SetLocation(StatesGroup):
    set_location_type = State()
    set_city = State()
    set_latitude = State()
    set_longitude = State()


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer("Добро пожаловать в Weather_bot!", reply_markup=reply.start_keyboard)


@dp.message(F.text == "Текущая погода")
async def get_current_weather(message: types.Message, state: FSMContext):
    pass


@dp.message(F.text == "Прогноз погоды")
async def get_forecast_weather(message: types.Message, state: FSMContext):
    pass


@dp.message(F.text == "Загрязнение воздуха")
async def get_air_polution(message: types.Message, state: FSMContext):
    pass


@dp.message(F.text == "Добавить оповещения")
async def add_notifications(message: types.Message, state: FSMContext):
    pass


@dp.message(F.text == "Мои оповещения")
async def my_notifications(message: types.Message, state: FSMContext):
    pass


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
