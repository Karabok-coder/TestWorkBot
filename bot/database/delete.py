from sqlalchemy.orm import sessionmaker

from loguru import logger

from bot.loader.load import engine
from bot.database import model


@logger.catch
async def deleteChatId(id: int):
    session = sessionmaker(bind=engine)
    with session() as s:
        try:
            s.query(model.Chat).filter(model.Chat.id == id).delete()
            s.commit()
            return True
        except Exception as e:
            logger.error(str(e))
            return False
        finally:
            session.close_all()
            