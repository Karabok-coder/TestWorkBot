from loguru import logger
from datetime import datetime, timedelta

from bot.loader.load import bot
from bot.util.doUser import SingleDoUser
from bot.database import select


@logger.catch
async def checkUserDo():
    logger.info("че то делаю")
    singleDoUser = SingleDoUser()
    for key in singleDoUser.do:
        item = singleDoUser.do[key]
        userId = key
        do = item['do']
        date = item['date']
        if datetime.now() >= date + timedelta(hours=1):
            user = await select.userIdUser(userId)
            text = f"Пользователь {userId} делает уже целый час: \"{do}\""
            await bot.send_message(user.managerId, text)