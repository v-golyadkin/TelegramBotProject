@echo off

call %~dp0Telegram_Bot_Project\venv\Scripts\activate

cd %~dp0Telegram_Bot_Project

set BOT_TOKEN=*******

set OPENAI_TOKEN=******

python telegram_bot.py

pause