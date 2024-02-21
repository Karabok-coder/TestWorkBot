from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callback.factory import ChatFactory

def choiseChat() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Назад",
        callback_data=ChatFactory(action="backChat", value=-1)
    )
    builder.button(
        text="Начать диалог",
        callback_data=ChatFactory(action="startChat", value=0)
    )
    builder.button(
        text="Вперед",
        callback_data=ChatFactory(action="nextChat", value=1)
    )

    return builder.as_markup()