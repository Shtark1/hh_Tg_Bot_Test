from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# КНОПКИ МЕНЮ
btn_profile = KeyboardButton("Профиль")
btn_info = KeyboardButton("О проекте")
btn_help = KeyboardButton("Help")


BUTTON_TYPES = {
    "BTN_HOME": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_profile, btn_info).add(btn_help)
}