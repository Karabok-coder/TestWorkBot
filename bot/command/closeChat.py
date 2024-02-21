from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loguru import logger

from bot.command.midleware import chatFilter, userFilter
from bot.util.chat import SingleChat
from bot.loader.load import bot
from bot.data.config import TEXT
from bot.keyboards import reply


router = Router()
router.message.middleware(chatFilter.IsActiveChat())

@router.message(F.text == TEXT['closeChat'])
@logger.catch
async def closeChatM(message: Message, state: FSMContext):
    await state.clear()
    singleChat = SingleChat()
    for chat in singleChat.chats:
        user = chat[0]
        manager = chat[1]
        if user == message.from_user.id:
            singleChat.closeChat(user, manager)
            await bot.send_message(manager, f"Чат завершен пользователем {user}", reply_markup=reply.manager())
            await message.answer("Чат завершен", reply_markup=reply.user())
            return
        elif manager == message.from_user.id:
            singleChat.closeChat(user, manager)
            await bot.send_message(user, f"Чат завершен пользователем {manager}", reply_markup=reply.user())
            await message.answer("Чат завершен", reply_markup=reply.manager())
            return
