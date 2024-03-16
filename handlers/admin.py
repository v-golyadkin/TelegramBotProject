from email import message
from lib2to3.pgen2.token import EQUAL
from aiogram import Dispatcher, types
from create_bot import dp

from aiogram.dispatcher.filters import Text
from keyboards import admin_keyboard,remove_keyboard


import os


token=os.getenv('BOT_TOKEN')



async def command_admin_menu(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Выберите что вы хотите сделать",reply_markup=admin_keyboard)
    else:
        await message.answer('Данная функция работает только в личных сообщениях с ботом')


async def command_clear_admin_menu(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Меню убрано",reply_markup=remove_keyboard)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_admin_menu, commands=['admin'], state=None)
    dp.register_message_handler(command_clear_admin_menu, Text(equals="Закрыть меню"))