from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import random
from loguru import logger

from bot.command.midleware.userFilter import IsAdmin, IsManager
from bot.data.config import TEXT_KB_ADMIN, ADMINS
from bot.keyboards import reply
from bot.database import select, insert
from bot.util.chat import SingleChat

router = Router()

@router.message(F.text == TEXT_KB_ADMIN['start'])
@router.message(F.text == TEXT_KB_ADMIN['menu'])
@router.message(F.text == '/start')
@logger.catch
async def choiseStart(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        await cmdStartAdmin(message, state)
        return
    elif bool(await select.userIdManager(message.from_user.id)):
        await cmdStartManager(message, state)
        return
    else:
        await cmdStartUser(message, state)
        return

@logger.catch
async def cmdStartAdmin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Добро пожаловать администратор!", reply_markup=reply.admin(message))

@logger.catch
async def cmdStartManager(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Добро пожаловать менеджер!", reply_markup=reply.manager())

@logger.catch
async def cmdStartUser(message: Message, state: FSMContext):
    await state.clear()
    singleChat = SingleChat()

    logger.debug(singleChat.chats)

    if not bool(await select.userIdUser(message.from_user.id)):
        await message.answer("Добро пожаловать новый пользователь!", reply_markup=reply.user())
        managers = await select.allManagers()
        await insert.insertUser(
            message.from_user.id,
            message.from_user.username,
            random.choice(managers).userId
        )
        return

    await message.answer("Добро пожаловать пользователь!", reply_markup=reply.user())