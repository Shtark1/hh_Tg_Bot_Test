from telegram_bot.utils import StatesSaveProducts



first_stat_message = "привет, ты тут первый раз, но мы тебя уже зарегистрировали, можешь потыкать на кнопки!"
second_stat_message = "Снова ты:)"
help_message = """<b><u>Отправь мне голосовое сообщение</u></b>
и я сохраню его в базу данных под твоим индификатором, так же конвертирую все аудио сообщения
в формат wav с частотой дискретизации 16kHz

<b><u>Отправь мне фото и я определю есть ли на нём лицо</u></b>
Если на фото есть лицо, я его сохраню"""
about_the_project_message = """
Этот не большой проект создан с целью прохождения тестового задания на вакансию 
Data Collection Specialist (Junior Python Developer)

<a href='https://github.com/Shtark1'>GitHub</a> - здесь вы можете посмотреть мои проекты
<a href='https://tosno.hh.ru/resume/90f06155ff0b85f9aa0039ed1f6d753530335a'>hh</a> - моё резюме
"""
unknown_command_message = "Я не знаю такой команды(\n Напиши /start или /help "
photo_processing_message = "Пожалуйста подождите...\nОбработка фото займёт несколько секунд!"

MESSAGES = {
    "start": first_stat_message,
    "second_start": second_stat_message,
    "help": help_message,
    "about_the_project": about_the_project_message,
    "unknown_command": unknown_command_message,
    "photo_processing": photo_processing_message,
}
