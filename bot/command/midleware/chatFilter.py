from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from loguru import logger

from bot.data.config import ADMINS
from bot.util.chat import SingleChat
from bot.database import select

class IsActiveChat(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        userId = data['event_from_user'].id
        singleChat = SingleChat()
        
        for chat in singleChat.chats:
            if chat[0] == userId:
                return await handler(event, data)
            elif chat[1] == userId:
                return await handler(event, data)