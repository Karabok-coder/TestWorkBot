from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from aiogram.types import Message

from loguru import logger

from bot.command.midleware import userFilter
from bot.database import insert
from bot.data.config import TEXT
from bot.keyboards import reply
from bot.database import select


router = Router()
router.message.middleware(userFilter.IsAdmin())

class NewManager(StatesGroup):
    userId = State()
    userTag = State()
    end = State()



@router.message(NewManager.userId)
@logger.catch
async def customer(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Id должно быть числом")
        return
    elif len(await select.userIdManager(int(message.text))) > 0:
        await message.answer("Такой пользователь уже существует")
        return

    await message.answer("Напишите тег пользователя")
    await state.update_data(userId=int(message.text))
    await state.set_state(NewManager.userTag)

@router.message(NewManager.userTag)
@logger.catch
async def executor(message: Message, state: FSMContext) -> None:
    if message.text.find('@') == -1:
        await message.answer("Тег должен начиниться с символа \"@\"")
        return

    await message.answer("Все ли верно?", reply_markup=reply.yes())
    await state.update_data(userTag=message.text)

    data = await state.get_data()
    userId = data['userId']
    userTag = data['userTag']

    await message.answer(f"Id: {userId}\nТег: {userTag}")
    await state.set_state(NewManager.end)


@router.message(NewManager.end)
@logger.catch
async def customer(message: Message, state: FSMContext) -> None:
    if message.text == TEXT['yes']:
        data = await state.get_data()    
        userId = data['userId']
        userTag = data['userTag']

        await insert.insertManager(userId, userTag)

        await message.answer("Новый менеджер успешно добавлен", reply_markup=reply.admin(message))
        await state.clear()
    else:
        await message.answer("Действие отменено", reply_markup=reply.admin(message))
        await state.clear()