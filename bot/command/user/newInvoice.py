from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loguru import logger

from bot.data.config import TEXT_KB_USER
from bot.keyboards import reply
from bot.states import stateInvoice

router = Router()

@router.message(F.text == TEXT_KB_USER['new_invoice'])
@router.message(F.text == '/new_invoice')
@logger.catch
async def choiseStart(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Напишите описание", reply_markup=reply.menu())
    await state.set_state(stateInvoice.NewInvoice.description)