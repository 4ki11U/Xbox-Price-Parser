from keyboards.reply import reply_keyboards
from keyboards.inline import inline_keyboards
from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from conductor import dp, bot

from additional.parser import parser
from datetime import datetime


@dp.message_handler(Text(equals=['Найти халяву !', 'Адрес регионов']))
async def start(message: types.Message, state: FSMContext):
    if message.text == 'Найти халяву !':
        await message.reply('Минутку, проверяю...')
        result_from_parsing = parser()
        day_today = datetime.now().strftime('%d-%m-%Y')
        mess_td = 'Состоянием на ' + f'<b>{day_today}</b>' + ' нашел такую халяву :\n<i>Для их получения просто перейди по ссылке и забери их</i>\n\n'

        pretty_message = mess_td + " ,  ".join(
            f'<a href="{value}">{key}</a>' for key, value in result_from_parsing.items())
        await message.answer(pretty_message, parse_mode='HTML', disable_notification=True)
    elif message.text == 'Адрес регионов':
        await message.reply('Выбери регион ниже 👇', reply_markup=inline_keyboards.inline_region_kb())
    else:
        await message.answer('Я пока не знаю как на это реагировать :(', reply_markup=types.ReplyKeyboardRemove())
