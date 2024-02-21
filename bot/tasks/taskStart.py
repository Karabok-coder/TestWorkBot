import asyncio
import aioschedule

from loguru import logger

from bot.tasks import checkUserDo


@logger.catch
async def start_schedule():
    try:
        aioschedule.clear()
        
        tag = f"checkUserDo"
        job = aioschedule.every().hour.do(checkUserDo.checkUserDo)
        job.tags = {tag}
            
        logger.info('Задачи установлены')
    except Exception as e:
        logger.error(e)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3)