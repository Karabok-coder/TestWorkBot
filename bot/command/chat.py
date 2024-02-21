from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loguru import logger

from bot.command.midleware import chatFilter
from bot.util.chat import SingleChat
from bot.loader.load import bot
from bot.keyboards import reply

router = Router()
router.message.middleware(chatFilter.IsActiveChat())

@router.message(F.text)
@logger.catch
async def choiseStart(message: Message, state: FSMContext):
    await state.clear()
    
    singleChat = SingleChat()
    
    for chat in singleChat.chats:
        if chat[0] == message.from_user.id:
            await bot.send_message(chat_id=chat[1], text=message.text)
        elif chat[1] == message.from_user.id:
            await bot.send_message(chat_id=chat[0], text=message.text)