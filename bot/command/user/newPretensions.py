from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loguru import logger

from bot.data.config import TEXT_KB_USER
from bot.keyboards import reply
from bot.states import statePretensions

router = Router()

@router.message(F.text == TEXT_KB_USER['new_pretensions'])
@router.message(F.text == '/new_pretensions')
@logger.catch
async def choiseStart(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Напишите номер накладной", reply_markup=reply.menu())
    await state.set_state(statePretensions.NewPretensions.invoiceNumber)