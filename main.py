from aiogram.dispatcher.dispatcher import Dispatcher

import asyncio
from loguru import logger

#Admin
from bot.command.admin import newManager
#Manager
from bot.command.manager import startChat, getPretensions
#User
from bot.command.user import newInvoice, queryManager, newPretensions
#Command
from bot.command import closeChat, start, chat

# callback
from bot.callback import callChat

from bot.states import stateNewManager, stateInvoice, statePretensions


from bot.loader.load import dp, bot

from bot.database import model
from bot.tasks import taskStart

async def on_startup(dispatcher: Dispatcher):
    logger.info('Bot on')
    asyncio.create_task(taskStart.start_schedule())
    await model.create_tables()

    dp.include_routers(start.router,
                       newManager.router,
                       newPretensions.router,
                       stateNewManager.router,
                       stateInvoice.router,
                       getPretensions.router,
                       statePretensions.router,
                       newInvoice.router,
                       startChat.router,
                       closeChat.router,
                       callChat.router,
                       queryManager.router,
                       chat.router)
    

async def on_shutdown(dispatcher: Dispatcher):
    logger.info('Bot off')

@logger.catch
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":    
    asyncio.run(main())