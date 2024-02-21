from aiogram.types import ReplyKeyboardMarkup, Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.data.config import ADMINS, TEXT_KB_ADMIN, TEXT_KB_USER, TEXT_KB_MANAGER, TEXT
from bot.database import select


def admin(message: Message) -> ReplyKeyboardMarkup:
    if str(message.from_user.id) in ADMINS:
        kb = ReplyKeyboardBuilder()
        kb.button(text=TEXT_KB_ADMIN['start'])
        kb.button(text=TEXT_KB_ADMIN['new_manager'])
        kb.adjust(2)
        return kb.as_markup(resize_keyboard=True)
    
def manager() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=TEXT_KB_MANAGER['start'])
    kb.button(text=TEXT_KB_MANAGER['chats'])
    kb.button(text=TEXT_KB_MANAGER['get_pretensions'])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
    
def user() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text=TEXT_KB_USER['start']),
        KeyboardButton(text=TEXT_KB_USER['new_invoice']),
        KeyboardButton(text=TEXT_KB_USER['query_manager']),
        KeyboardButton(text=TEXT_KB_USER['new_pretensions'])
    )
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
    
def menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=TEXT_KB_ADMIN['menu'])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
    
def yes() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='✅ Да')
    kb.button(text='❌ Нет')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
    
def payment() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='💳 Безналичный')
    kb.button(text='💵 Наличный')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def endChat() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=TEXT['closeChat'])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)