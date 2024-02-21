from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loguru import logger

from bot.command.midleware.userFilter import IsAdmin
from bot.data.config import TEXT_KB_ADMIN
from bot.keyboards import reply
from bot.states import stateNewManager


router = Router()
router.message.middleware(IsAdmin())

@router.message(F.text == TEXT_KB_ADMIN['new_manager'])
@router.message(F.text == '/new_manager')
@logger.catch
async def cmdNewManager(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Напишите Id нового менеджера", reply_markup=reply.menu())
    await state.set_state(stateNewManager.NewManager.userId)