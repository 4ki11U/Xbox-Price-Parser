from aiogram.types import ReplyKeyboardMarkup

### --- Start Button --- ###
start_main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).row('Найти халяву !').add('Адрес регионов').add('Тестовая кнопка')
