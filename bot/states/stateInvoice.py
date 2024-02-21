from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, BufferedInputFile

from datetime import datetime
from loguru import logger

from bot.database import insert
from bot.data.config import TEXT
from bot.keyboards import reply
from bot.util import pdf
from bot.util.doUser import SingleDoUser

router = Router()

class NewInvoice(StatesGroup):
    description = State()
    mass = State()
    volume = State()
    shipping = State()
    receiving = State()
    payment = State()
    end = State()

@router.message(NewInvoice.description)
@logger.catch
async def description(message: Message, state: FSMContext) -> None:
    SingleDoUser().addDo(message.from_user.id, "Заполняет описание накладной", datetime.now())
    await message.answer("Напишите вес груза")
    await state.update_data(description=message.text)
    await state.set_state(NewInvoice.mass)

@router.message(NewInvoice.mass)
@logger.catch
async def mass(message: Message, state: FSMContext) -> None:
    SingleDoUser().addDo(message.from_user.id, "Заполняет вес груза", datetime.now())
    await message.answer("Напишите габариты груза")
    await state.update_data(mass=message.text)
    await state.set_state(NewInvoice.volume)

@router.message(NewInvoice.volume)
@logger.catch
async def volume(message: Message, state: FSMContext) -> None:
    SingleDoUser().addDo(message.from_user.id, "Заполняет габариты груза", datetime.now())
    await message.answer("Напишите точный адрес отправки")
    await state.update_data(volume=message.text)
    await state.set_state(NewInvoice.shipping)

@router.message(NewInvoice.shipping)
@logger.catch
async def shipping(message: Message, state: FSMContext) -> None:
    SingleDoUser().addDo(message.from_user.id, "Заполняет адрес отправки", datetime.now())
    await message.answer("Напишите точный адрес получения")
    await state.update_data(shipping=message.text)
    await state.set_state(NewInvoice.receiving)

@router.message(NewInvoice.receiving)
@logger.catch
async def receiving(message: Message, state: FSMContext) -> None:
    SingleDoUser().addDo(message.from_user.id, "Заполняет адрес получения", datetime.now())
    await message.answer("Выберите способ оплаты", reply_markup=reply.payment())
    await state.update_data(receiving=message.text)
    await state.set_state(NewInvoice.payment)

@router.message(NewInvoice.payment)
@logger.catch
async def payment(message: Message, state: FSMContext) -> None:
    SingleDoUser().addDo(message.from_user.id, "Выберает способ оплаты", datetime.now())
    if message.text == TEXT['cash']:
        await state.update_data(payment=TEXT['cash'])
        await state.set_state(NewInvoice.end)
    elif message.text == TEXT['cashless']:
        await state.update_data(payment=TEXT['cashless'])
        await state.set_state(NewInvoice.end)
    else:
        await message.answer("Выберите между наличной и безналичной оплатой")
        return

    await message.answer("Все ли верно", reply_markup=reply.yes())

    data = await state.get_data()

    payment = TEXT["cashless"] if bool(data['payment']) else TEXT["cash"]

    text = f"Описание: {data['description']}\n" + \
           f"Вег груза: {data['mass']}\n" + \
           f"Габариты груза: {data['volume']}\n" + \
           f"Адрес отправки: {data['shipping']}\n" + \
           f"Адрес получения: {data['receiving']}\n" + \
           f"Способ оплаты: {payment}\n"
    
    await message.answer(text)

@router.message(NewInvoice.end)
@logger.catch
async def end(message: Message, state: FSMContext) -> None:
    SingleDoUser().addDo(message.from_user.id, "Проверяет накладную", datetime.now())
    if message.text == TEXT['yes']:
        data = await state.get_data()
        await insert.insertInvoice(
            data['description'],
            data['mass'],
            data['volume'],
            data['shipping'],
            data['receiving'],
            data['payment']
        )

        dataPdf = {
            "Описание" : data['description'],
            "Вес груза" : data['mass'],
            "Габариты" : data['volume'],
            "Адрес отправки" : data['shipping'],
            "Адрес получения" : data['receiving'],
            "Способ оплаты" : data['payment'].split(' ')[1]
        }

        pdfFile = await pdf.generate_pdf(dataPdf)
        await message.answer_document(BufferedInputFile(pdfFile, "Наклодная.pdf"), caption="Новая накладная успешно создана")
    elif message.text == TEXT['no']:
        await message.answer("Изменения не сохранены")
    else:
        await message.answer("Выберите между да и нет")

    await state.clear()