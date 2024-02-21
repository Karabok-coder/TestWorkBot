from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loguru import logger

from bot.data.config import TEXT_KB_USER
from bot.keyboards import reply
from bot.states import stateInvoice
from bot.database import insert, select
from bot.loader.load import bot

router = Router()

@router.message(F.text == TEXT_KB_USER['query_manager'])
@router.message(F.text == '/query_manager')
@logger.catch
async def queryManager(message: Message, state: FSMContext):
    await state.clear()
    userId = message.from_user.id
    user = await select.userIdUser(userId)
    await insert.insertChat(userId, user.managerId)
    await bot.send_message(user.managerId, text=f"Пользователь Id: {userId} просит связаться")
    await message.answer("Менеджер вызыван, ожидайте ответа")