from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from loguru import logger

from bot.data.config import ADMINS
from bot.database import select


class IsAdmin(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        userId = data['event_from_user'].id
        if str(userId) in ADMINS:
            return await handler(event, data)

class IsManager(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        userId = data['event_from_user'].id
        managers = await select.allManagers()

        if managers is None:
            return

        for manager in managers:
            if userId == manager.userId:
                return await handler(event, data)