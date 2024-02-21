from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loguru import logger

from bot.database import select
from bot.command.midleware import userFilter
from bot.keyboards import inline
from bot.data.config import TEXT_KB_MANAGER


router = Router()
router.message.middleware(userFilter.IsManager())

@router.message(F.text == TEXT_KB_MANAGER['chats'])
@router.message(F.text == "/chats")
@logger.catch
async def startChat(message: Message, state: FSMContext):
    await state.clear()
    chats = await select.chatManagerId(message.from_user.id)
    if len(chats) == 0:
        await message.answer("Сейчас нет активных вызовов")
        return
    await message.answer(
        f"#0 \nПользователь Id: {chats[0].userId}",
        reply_markup=inline.choiseChat()
    )