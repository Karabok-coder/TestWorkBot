from sqlalchemy.orm import sessionmaker, Query

from loguru import logger

from bot.loader.load import engine
from bot.database import model


@logger.catch
async def allManagers():
    session = sessionmaker(bind=engine)
    with session() as s:
        result = s.query(model.Manager).all()
    session.close_all()
    return result

@logger.catch
async def userIdManager(userId: int):
    session = sessionmaker(bind=engine)
    with session() as s:
        result = s.query(model.Manager).filter(model.Manager.userId == userId).all()
    session.close_all()
    return result

@logger.catch
async def userIdUser(userId: int):
    session = sessionmaker(bind=engine)
    with session() as s:
        result = s.query(model.User).filter(model.User.userId == userId).first()
    session.close_all()
    return result

@logger.catch
async def chatUserId(userId: int):
    session = sessionmaker(bind=engine)
    with session() as s:
        result = s.query(model.Chat).filter(model.Chat.userId == userId).all()
    session.close_all()
    return result

@logger.catch
async def chatManagerId(managerId: int):
    session = sessionmaker(bind=engine)
    with session() as s:
        result = s.query(model.Chat).filter(model.Chat.managerId == managerId).all()
    session.close_all()
    return result

@logger.catch
async def pretensionsUserId(userId: int):
    session = sessionmaker(bind=engine)
    with session() as s:
        result = s.query(model.Pretension).filter(model.Pretension.userId == userId).all()
    session.close_all()
    return result

@logger.catch
async def allPretensions():
    session = sessionmaker(bind=engine)
    with session() as s:
        result = s.query(model.Pretension).all()
    session.close_all()
    return result