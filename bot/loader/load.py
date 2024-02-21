from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.enums.parse_mode import ParseMode

from loguru import logger

from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import create_engine 

from bot.data.config import TOKEN, PATH_LOGS, PATH_DATABASE


bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

logger.add(PATH_LOGS,
           format='{time}, {level}, {file}, {module}, {line}, {function}, {message}', 
           level="DEBUG", 
           rotation="10 MB", 
           compression="zip")

engine = create_engine(f"sqlite+pysqlite:///{PATH_DATABASE}", echo=False)
Base = declarative_base()