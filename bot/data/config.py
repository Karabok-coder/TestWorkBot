import configparser
import os

import os.path

# Пути до файлов
PATH_LOGS = os.path.abspath('bot/data/logs/log.log')
PATH_DATABASE = os.path.abspath('bot/data/database.db')
PATH_SETTINGS = os.path.abspath('settings.ini')
PATH_FONT = os.path.abspath('bot/data/Arial.ttf')
read_config = configparser.ConfigParser()
read_config.read(PATH_SETTINGS)

# Переменные из настроек
ADMINS = read_config['settings']['admins'].strip().split(' ') # админы
TOKEN = read_config['settings']['token'] # Токен бота
BOT_VERSION = read_config['settings']['bot_version'] # Версия бота


TEXT_KB_ADMIN = {
    'start' : '🔁 Перезапуск',
    'new_manager' : '👷‍♂️ Новый менеджер',
    'menu' : '🏠 Главное меню',    
    # '' : '',
    # '' : '',
    # '' : '',
}

TEXT_KB_USER = {
    'start' : '🔁 Перезапуск',
    'menu' : '🏠 Главное меню',
    'new_invoice' : '📘 Новавя накладная',
    'query_manager' : '📞 Вызывать менеджера',
    'new_pretensions' : '⚠️ Новая претензия',
    # '' : '',
    # '' : '',
}

TEXT_KB_MANAGER = {
    'start' : '🔁 Перезапуск',
    'menu' : '🏠 Главное меню',
    'chats' : '📑 Чаты',
    'get_pretensions' : '🗄 Получить претензии',
    # '' : '',
    # '' : '',
}

TEXT = {
    'yes' : '✅ Да',
    'no' : '❌ Нет',
    'cash' : '💵 Наличный',
    'cashless' : '💳 Безналичный',
    'closeChat' : '❌ Завершить чат',
    # '' : '',
    # '' : '',
    # '' : '',
    # '' : '',
}