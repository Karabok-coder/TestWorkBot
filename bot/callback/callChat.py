from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loguru import logger

from bot.command.midleware import userFilter
from bot.callback.factory import ChatFactory
from bot.database import select, delete
from bot.util.chat import SingleChat
from bot.keyboards import reply, inline
from bot.loader.load import bot

router = Router()
router.message.middleware(userFilter.IsManager())

@router.callback_query(ChatFactory.filter())
@logger.catch
async def backChat(callback: CallbackQuery, callback_data: ChatFactory):
    chats = await select.chatManagerId(callback.from_user.id)
    countChat = int(callback.message.text.split('\n')[0].replace("#", ""))

    if callback_data.action == "startChat":
        singleChat = SingleChat()
        singleChat.addChat(chats[countChat].userId, chats[countChat].managerId)
        await delete.deleteChatId(chats[countChat].id)
        await callback.message.delete()
        await callback.message.answer(
                f"Чат с пользователем {chats[countChat].userId} начат",
                reply_markup=reply.endChat()
            )
        await bot.send_message(chats[countChat].userId, "Менеджер начал чат", reply_markup=reply.endChat())

    if not 0 <= (countChat + callback_data.value) < len(chats):
        await callback.message.edit_text(
            text=f"#{countChat}\nПользователь Id: {chats[countChat].userId}\nЭто последний чат!",
            reply_markup=inline.choiseChat()
        )
        return
        
    if callback_data.action == "backChat" or callback_data.action == "nextChat":
        countChat += callback_data.value
        await callback.message.edit_text(
            text=f"#{countChat}\nПользователь Id: {chats[countChat].userId}",
            reply_markup=inline.choiseChat()
        )