from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import types

admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
remove_keyboard = types.ReplyKeyboardRemove()
buttons_command=['Рассылка','Черный список']


button_edit=['Изменить черный список']
button_exit=['Закрыть меню']
admin_keyboard.add(*buttons_command).row(*button_edit).row(*button_exit)
