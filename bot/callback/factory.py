from typing import Optional
from aiogram.filters.callback_data import CallbackData

class ChatFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None