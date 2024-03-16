from email import message
from lib2to3.pgen2.token import EQUAL
from aiogram import Dispatcher, types
from create_bot import dp

from aiogram.dispatcher.filters import Text
from keyboards import client_keyboard,remove_keyboard

import speech_recognition as sr
import uuid
from pydub import AudioSegment
import tempfile

from create_bot import bot
import os

import openai 

from db import DataBase

r = sr.Recognizer()

db= DataBase("users.db")

token=os.getenv('BOT_TOKEN')

openai.api_key='*******'
messages=[
    {"role": "system", "content": "You are s chat bot"},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi"}]



def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are s chat bot"},
            {"role": "user", "content": prompt}]
        )
    return response.choices[0].message.content

async def send_private_chat(message : types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        update(messages, "user", message.text)
        responce = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
        )
        await message.answer(responce['choices'][0]['message']['content'])


async def send_group_chat(message : types.Message):
    if message.chat.type == 'group':
        update(messages, "user", message.text)
        responce_group = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
        )
        await message.answer(responce_group['choices'][0]['message']['content'])

async def handle_audio(message: types.Message):

    file_info = message.voice.file_id
    voice_file = await bot.get_file(file_info)
    voice_path = voice_file.file_path
    voice_data = await bot.download_file(voice_path)

    filename = f"{uuid.uuid4()}.wav"
    file_path = f"./voice/{filename}"

    with open(file_path, 'wb') as voice_file:
        voice_file.write(voice_data.getvalue())

    audio = AudioSegment.from_ogg(file_path)
    audio.export(file_path, format='wav')

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language='ru-RU')

        generated_text = generate_text(text)

        await message.answer(generated_text)
    except sr.UnknownValueError:
        await message.answer("Не удалось распознать речь.")
    except sr.RequestError as e:
        await message.answer(f"Ошибка сервиса распознавания речи: {e}")

    os.remove(file_path)

async def command_set_activity(message: types.Message):
        if db.get_user_activity(message.from_user.id)[0][0] == 1:
            db.set_activity(message.from_user.id,0)
            await message.answer("Рассылка была выключена")
        else:
            db.set_activity(message.from_user.id,1)
            await message.answer("Рассылка была включена")

async def command_activity_status(message: types.Message):
    if db.get_user_activity(message.from_user.id)[0][0] == 1:
        await message.answer("У вас включена рассылка")
    else:
        await message.answer("У вас выключена рассылка")

async def command_ignore_status(message: types.Message):
    if db.get_user_activity(message.from_user.id)[0][0] == 1:
        await message.answer("У вас включена рассылка")
    else:
        await message.answer("У вас выключена рассылка")

async def command_test1(message: types.Message):
    await message.answer(message.from_user.full_name)

async def command_test2(message: types.Message):
    await message.answer(message.from_user.url)

async def command_client_menu(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Выберите что хотите выбрать",reply_markup=client_keyboard)
    else:
        await message.answer('Данная функция работает только в личных сообщениях с ботом')

async def command_menu_about(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Меню убрано",reply_markup=remove_keyboard)

async def command_menu_help(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Меню убрано",reply_markup=remove_keyboard)

async def command_menu_comandlist(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Меню убрано",reply_markup=remove_keyboard)

async def command_clear_client_menu(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Меню убрано",reply_markup=remove_keyboard)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(handle_audio ,content_types=['voice'])
    dp.register_message_handler(command_set_activity, commands=['ignore'])
    dp.register_message_handler(command_activity_status, commands=['activity_status','activity','status'])
    dp.register_message_handler(command_ignore_status, commands=['ignore_status',])
    dp.register_message_handler(command_client_menu, Text(equals="/menu"))
    dp.register_message_handler(command_clear_client_menu, Text(equals="Закрыть меню"))
    dp.register_message_handler(command_menu_help, Text(equals="Помощь"))
    dp.register_message_handler(command_menu_comandlist, Text(equals="Список команд"))
    dp.register_message_handler(command_menu_about, Text(equals="О боте"))
    dp.register_message_handler(send_group_chat, commands=['send'])
    dp.register_message_handler(send_private_chat)

