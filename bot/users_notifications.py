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


class EditState(StatesGroup):
    time = State()
    utc = State()
    

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
        description += "Время: " + notification.notifications_time.strftime("%H:%M") + "\n"
        description += "Часовой пояс: " + notification.utc + "\n"
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
    await state.set_state(EditState.time)
    await state.update_data(notification_id=notification_id)
    await state.update_data(chat_id=chat_id)
    await bot.send_message(chat_id, "Укажите время для отправки оповещений в формате HH:MM:")


@router.callback_query(lambda c: c.data.startswith('change_utc_'))
async def set_new_utc_clicked(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    chat_id = callback_query.message.chat.id
    notification_id = int(callback_query.data.split('_')[2])
    await state.set_state(EditState.utc)
    await state.update_data(notification_id=notification_id)
    await state.update_data(chat_id=chat_id)
    await bot.send_message(chat_id, "Укажите часовой пояс в формате UTC+00:00:")


@router.message(F.text, StateFilter(EditState.time))
async def set_new_time(message: types.Message, state: FSMContext):
    pattern = r"^(0[0-9]|1[0-9]|2[0-3])[:-](0[0-9]|[1-5][0-9])$"
    if re.match(pattern, message.text):
        data = await state.get_data()
        notification_id = data.get("notification_id")
        chat_id = data.get("chat_id")
        session = db_helper.get_scoped_session()
        new_time = datetime.strptime(message.text, "%H:%M").time()
        updates = {"notifications_time": new_time}
        await crud.update_weather_notifications(chat_id, notification_id, updates, session)
        await message.answer(f"Вермя уведомления успешно изменено на {message.text}")
    else:
        await message.answer("Ошибка в формате времени, введите время в формате HH:MM!")


@router.message(F.text, StateFilter(EditState.utc))
async def set_new_utc(message: types.Message, state: FSMContext):   
    pattern = r"^UTC[+-](0[0-9]|1[0-4]):00$"
    if re.match(pattern, message.text, re.IGNORECASE):
        data = await state.get_data()
        chat_id = data.get("chat_id")
        notification_id = data.get("notification_id")
        session = db_helper.get_scoped_session()
        new_utc = message.text[:3].upper() + message.text[3:] 
        updates = {"utc": new_utc}
        await crud.update_weather_notifications(chat_id, notification_id, updates, session)
        await message.answer(f"Часовой пояс успешно изменён на {message.text}")
    else:
        await message.answer("Ошибка в формате часового пояса, введите часовой пояс в формате UTC+00:00!")
