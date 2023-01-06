import logging
from pathlib import Path
import os
import time
import re

from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types.message import ContentType

from telegram_bot.utils import StatesSaveProducts
from content_text.messages import MESSAGES
from telegram_bot.KeyboardButton import BUTTON_TYPES

from dop_functionals.face_recognition import face_analyze
from dop_functionals.converts_voice import converts_wav
from cfg.cfg import TOKEN
from cfg.database import Database

db = Database("cfg/database.sqlite3")

logging.basicConfig(format=u"%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s",
                    level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


# TODO ====================== Start =====================
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                    message.from_user.username)
        await message.answer(f"<u>{message.from_user.first_name}</u>, {MESSAGES['start']}",
                             reply_markup=BUTTON_TYPES["BTN_HOME"], parse_mode="HTML")
    else:
        await message.answer(MESSAGES["second_start"], reply_markup=BUTTON_TYPES["BTN_HOME"])


# TODO ===================== Buttons =====================
@dp.message_handler(lambda message: message.text.lower() == "профиль")
async def profile_info(message: Message):
    await message.answer(f"""<b>==== Инфо о тебе ====</b>
username: {message.from_user.username}
first_name: {message.from_user.first_name}
last_name: {message.from_user.last_name}
user_id: {message.from_user.id}
""", parse_mode="HTML")


@dp.message_handler(lambda message: message.text.lower() == "о проекте")
async def types_of_subscriptions(message: Message):
    await message.answer(MESSAGES["about_the_project"], reply_markup=BUTTON_TYPES["BTN_HOME"], parse_mode="HTML")


@dp.message_handler(lambda message: message.text.lower() == "help" or message.text.lower() == "/help")
async def help_command(message: Message):
    await message.answer(MESSAGES["help"], parse_mode="HTML")


# TODO ===================== Голосовое Сообщение ========================
@dp.message_handler(content_types='voice')
async def voice_message(message: types.Message):
    # if message.voice:
        await message.answer("Это голосовое сообщение!")
        voice_id = message.voice.file_id
        file_voice = await bot.get_file(voice_id)
        file_voice_path = file_voice.file_path

        i = 0
        while True:
            path = f"all_files/voice_mp3/{message.from_user.id}_{i}.mp3"
            if Path(path).exists():
                i += 1
            else:
                await bot.download_file(file_voice_path, path)
                break

        await converts_wav(path, f"all_files/voice_wav_16kHz/{message.from_user.id}_{i}")


# TODO ========================== ФОТО ==============================
@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    await message.answer(MESSAGES["photo_processing"])

    i = 0
    while True:
        path = f"all_files/photo/{message.from_user.id}_{i}.jpg"
        if Path(path).exists():
            i += 1
        else:
            await message.photo[-1].download(path)
            break

    info_foto = await face_analyze(path)
    if info_foto == "На этом фото нет лица человека!":
        await message.answer(info_foto)
    else:
        race = []
        emotions = []
        for k, v in info_foto[2].items():
            race.append(f'{k} - {round(v, 2)}%')

        for k, v in info_foto[3].items():
            emotions.append(f'{k} - {round(v, 2)}%')

        await message.answer(f"""<u>На фото есть лицо человека!</u>

<b>Возраст:</b> {info_foto[0]} 
<b>Пол:</b> {info_foto[1]}
<b>Раса:</b> """ + "\n           ".join(race) + """
<b>Эмоц:</b> """ + "\n            ".join(emotions), parse_mode="HTML")


# TODO ===================== Неизвестная Команда ========================
@dp.message_handler()
async def unknown_command(message: Message):
    await message.answer(MESSAGES["unknown_command"])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def start():
    executor.start_polling(dp, on_shutdown=shutdown)
