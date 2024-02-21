from sqlalchemy.orm import sessionmaker

from loguru import logger

from bot.loader.load import engine
from bot.database import model


@logger.catch
async def insertManager(userId: int, userTag: str):
    session = sessionmaker(bind=engine)
    with session() as s:
        query = model.Manager(userId=userId, userTag=userTag)
        try:
            s.add(query)
            s.commit()
            return True
        except Exception as e:
            logger.error(str(e))
            return None
        finally:
            session.close_all()

@logger.catch
async def insertUser(userId: int, userTag: str, managerId: int):
    session = sessionmaker(bind=engine)
    with session() as s:
        query = model.User(userId=userId, userTag=userTag, managerId=managerId)
        try:
            s.add(query)
            s.commit()
            return True
        except Exception as e:
            logger.error(str(e))
            return None
        finally:
            session.close_all()

@logger.catch
async def insertInvoice(description: str, mass: str, volume: str, shipping: str, receiving: str, payment: str):
    session = sessionmaker(bind=engine)
    with session() as s:
        query = model.Invoice(description=description, 
                              mass=mass, 
                              volume=volume, 
                              shipping=shipping, 
                              receiving=receiving,
                              payment=payment)
        try:
            s.add(query)
            s.commit()
            return True
        except Exception as e:
            logger.error(str(e))
            return None
        finally:
            session.close_all()

@logger.catch
async def insertChat(userId: int, managerId: int):
    session = sessionmaker(bind=engine)
    with session() as s:
        query = model.Chat(userId=userId,
                           managerId=managerId)
        try:
            s.add(query)
            s.commit()
            return True
        except Exception as e:
            logger.error(str(e))
            return None
        finally:
            session.close_all()

@logger.catch
async def insertPretensions(invoiceNumber: str, email: str, decsription: str, ammount: int, photos: str, userId: int):
    session = sessionmaker(bind=engine)
    with session() as s:
        query = model.Pretension(invoiceNumber=invoiceNumber,
                           email=email,
                           decsription=decsription,
                           ammount=ammount,
                           photos=photos,
                           userId=userId
                           )
        try:
            s.add(query)
            s.commit()
            return True
        except Exception as e:
            logger.error(str(e))
            return None
        finally:
            session.close_all()