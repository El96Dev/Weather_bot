from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards import reply


router = Router()

@router.message(F.text == "Мои оповещения")
async def my_notifications(message: types.Message, state: FSMContext):
    pass


