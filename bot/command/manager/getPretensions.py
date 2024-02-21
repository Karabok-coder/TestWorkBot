from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from loguru import logger
import csv
from io import BytesIO

from bot.database import select
from bot.command.midleware import userFilter
from bot.data.config import TEXT_KB_MANAGER


router = Router()
router.message.middleware(userFilter.IsManager())

@router.message(F.text == TEXT_KB_MANAGER['get_pretensions'])
@router.message(F.text == "/get_pretensions")
@logger.catch
async def startChat(message: Message, state: FSMContext):
    await state.clear()
    header = ["Номер накладной", "Почта", "Описание", "Количесвто", "Фото", "Пользователь"]
    with open('output.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)

    pretensions = await select.allPretensions()
    for pretension in pretensions:
        user = await select.userIdUser(pretension.userId)
        if user.managerId == message.from_user.id:
            with open('output.csv', 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)

                csvwriter.writerow([
                    pretension.invoiceNumber,
                    pretension.email,
                    pretension.decsription,
                    pretension.ammount,
                    pretension.photos,
                    pretension.userId
                    ])
                
    with open('output.csv', 'rb') as csvfile:
        await message.answer_document(BufferedInputFile(csvfile.read(), 'Претензии.csv'))