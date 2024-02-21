from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from aiogram.types import Message

from loguru import logger

from bot.database import insert, select
from bot.data.config import TEXT
from bot.keyboards import reply
from bot.loader.load import bot


router = Router()

class NewPretensions(StatesGroup):
    invoiceNumber = State()
    email = State()
    description = State()
    ammount = State()
    photos = State()
    end = State()


@router.message(NewPretensions.invoiceNumber)
@logger.catch
async def customer(message: Message, state: FSMContext) -> None:
    await message.answer("Напишите электронную почту")
    await state.update_data(invoiceNumber=message.text)
    await state.set_state(NewPretensions.email)

@router.message(NewPretensions.email)
@logger.catch
async def customer(message: Message, state: FSMContext) -> None:
    await message.answer("Напишите описание")
    await state.update_data(email=message.text)
    await state.set_state(NewPretensions.description)

@router.message(NewPretensions.description)
@logger.catch
async def customer(message: Message, state: FSMContext) -> None:
    await message.answer("Напишите количество")
    await state.update_data(description=message.text)
    await state.set_state(NewPretensions.ammount)

@router.message(NewPretensions.ammount)
@logger.catch
async def customer(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Количесвто должно быть целым числом")
        return
    await message.answer("Отравьте фото")
    await state.update_data(ammount=int(message.text))
    await state.set_state(NewPretensions.photos)

@router.message(NewPretensions.photos)
@logger.catch
async def customer(message: Message, state: FSMContext) -> None:
    await state.update_data(photos=message.photo[0].file_id)
    
    await message.answer("Все ли верно?", reply_markup=reply.yes())

    data = await state.get_data()

    text = f"Номер накладной: {data['invoiceNumber']}\n" + \
           f"Почта: {data['email']}\n" + \
           f"Описание: {data['description']}\n" + \
           f"Количество: {data['ammount']}"
    
    await message.answer_photo(message.photo[0].file_id, text)
    await state.set_state(NewPretensions.end)

@router.message(NewPretensions.end)
@logger.catch
async def customer(message: Message, state: FSMContext) -> None:
    if message.text == TEXT['yes']:
        data = await state.get_data()
        userId = message.from_user.id

        await insert.insertPretensions(
                data['invoiceNumber'], 
                data['email'],
                data['description'],
                data['ammount'],
                data['photos'],
                userId
            )
                
        text = f"Новая претензия от пользователя {userId}:\n" + \
               f"Номер накладной: {data['invoiceNumber']}\n" + \
               f"Почта: {data['email']}\n" + \
               f"Описание: {data['description']}\n" + \
               f"Количество: {data['ammount']}"

        user = await select.userIdUser(userId)
        await bot.send_photo(user.managerId, data['photos'], caption=text)

        await message.answer("Претензия успешно добавлена", reply_markup=reply.user())
        await state.clear()
    else:
        await message.answer("Действие отменено", reply_markup=reply.user())
        await state.clear()