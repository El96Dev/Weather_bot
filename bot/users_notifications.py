import re
from datetime import datetime

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import crud
from models import NotificationsType
from db_helper import db_helper
from keyboards import reply
from keyboards.notifications_time_keyboard import notifications_time_keyboard
from models import NotificationsTime
from load_config import config


class EditState(StatesGroup):
    set_new_time = State()
    

router = Router()

@router.message(F.text == "Мои оповещения")
async def my_notifications(message: types.Message, state: FSMContext):
    session = db_helper.get_scoped_session()
    notifications = await crud.get_weather_notifications(message.chat.id, session)
    if len(notifications) == 0:
        await message.reply("У Вас пока нет уведомлений.")
    for notification in notifications:
        description = ""
        description += ("Текущая погода" if notification.notifications_type == NotificationsType.CURRENT else "Прогноз погоды") + "\n"
        description += "Время: " + config.get_notifications_time_value(notification.notifications_time) + "\n"
        description += "Локация: " + notification.city
        keyboard = reply.inline_keyboard_for_notifications(notification.id)
        await message.reply(description, reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith('delete_'))
async def delete_notification(callback_query: types.CallbackQuery, bot: Bot):
    notification_id = int(callback_query.data.split('_')[1])
    chat_id = callback_query.message.chat.id
    session = db_helper.get_scoped_session()
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await crud.delete_weather_notifications(chat_id, notification_id, session)
    await bot.answer_callback_query(callback_query.id, "Уведомление успешно удалено!")


@router.callback_query(lambda c: c.data.startswith('change_time_'))
async def set_new_time_clicked(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    chat_id = callback_query.message.chat.id
    notification_id = int(callback_query.data.split('_')[2])
    await state.set_state(EditState.set_new_time)
    await state.update_data(notification_id=notification_id)
    await state.update_data(chat_id=chat_id)
    await bot.send_message(chat_id, "Выберите новое время для отправки оповещений:", 
                           reply_markup=notifications_time_keyboard.get_notifications_time_keyboard())


@router.message(F.text, StateFilter(EditState.set_new_time))
async def set_new_time(message: types.Message, state: FSMContext):
    if notifications_time_keyboard.get_notifications_time_keyboard(message.text):
        if message.text == f"Утренние - {config.morning.get_notifications_time()}":
            await state.update_data(notifications_time=NotificationsTime.MORNING) 
        elif message.text == f"Дневные - {config.day.get_notifications_time()}":
            await state.update_data(notifications_time=NotificationsTime.DAY)
        elif message.text == f"Вечерние - {config.evening.get_notifications_time()}":
            await state.update_data(notifications_time=NotificationsTime.EVENING)

        data = await state.get_data()
        notification_id = data.get("notification_id")
        chat_id = data.get("chat_id")
        session = db_helper.get_scoped_session()
        new_time = data.get("notifications_time")
        updates = {"notifications_time": new_time}
        await crud.update_weather_notifications(chat_id, notification_id, updates, session)
        await message.answer(f"Вермя уведомления успешно изменено на {message.text[-5:]}")

    else:
        await message.answer("Выберите один из предоставленных вариантов!",
                             reply_markup=notifications_time_keyboard.get_notifications_time_keyboard())


