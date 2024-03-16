from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import types

client_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
remove_keyboard = types.ReplyKeyboardRemove()
buttons_command=['Список команд','Помощь']


button_edit=['О боте']
button_exit=['Закрыть меню']
client_keyboard.add(*buttons_command).row(*button_edit).row(*button_exit)