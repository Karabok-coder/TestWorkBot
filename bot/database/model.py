from sqlalchemy import Column, Integer, String, Boolean, BIGINT, ForeignKey
from bot.loader.load import Base, engine
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'Users'

    userId = Column(BIGINT, primary_key=True)
    userTag = Column(String(250))
    managerId = Column(BIGINT, ForeignKey("Managers.userId"), nullable=False)
    
    parent = relationship("Manager", back_populates="users")

class Manager(Base):
    __tablename__ = 'Managers'

    userId = Column(BIGINT, primary_key=True)
    userTag = Column(String(250))

    users = relationship("User", back_populates="parent")

class Pretension(Base):
    __tablename__ = "Pretensions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    invoiceNumber = Column(String(128))
    email = Column(String(128))
    decsription = Column(String(512))
    ammount = Column(Integer)
    photos = Column(String(512))
    userId = Column(BIGINT, ForeignKey("Users.userId"))

class Invoice(Base):
    __tablename__ = "Invoice"

    id = Column(Integer, primary_key=True, autoincrement=True)

    description = Column(String(512))
    mass = Column(String(128))
    volume = Column(String(128))
    shipping = Column(String(128))
    receiving = Column(String(128))
    payment = Column(String(32))

class Chat(Base):
    __tablename__ = "Chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    managerId = Column(BIGINT, ForeignKey("Managers.userId"))
    userId = Column(BIGINT, ForeignKey("Users.userId"))

async def create_tables():
    Base.metadata.create_all(engine)