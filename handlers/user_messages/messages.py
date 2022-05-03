from aiogram.utils import exceptions

from config_files.config import xprices_channel
from keyboards.reply import reply_keyboards
from keyboards.inline import inline_keyboards
from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from conductor import dp, bot

from additional.parser import parse_site_xbox_now, search_new_deals
from datetime import datetime
import json
from asyncio import sleep

from aiofiles import os


@dp.message_handler()
@dp.message_handler(Text(equals=['Найти халяву !', 'Адрес регионов', 'Тестовая кнопка']))
async def start(message: types.Message):
    if message.text == 'Найти халяву !':
        await message.reply('Минутку, проверяю...')
        result_from_parsing = parser()
        day_today = datetime.now().strftime('%d-%m-%Y')
        mess_td = 'Состоянием на ' + f'<b>{day_today}</b>' + ' нашел такую халяву :\n<i>Для их получения просто перейди по ссылке и забери их</i>\n\n'

        pretty_message = mess_td + " ,  ".join(f'<a href="{value}">{key}</a>' for key, value in result_from_parsing.items())
        await message.answer(pretty_message, parse_mode='HTML', disable_notification=True)
    elif message.text == 'Адрес регионов':
        await message.reply('Выбери регион ниже 👇', reply_markup=inline_keyboards.inline_region_kb())
    elif message.text == 'Тестовая кнопка':
        await message.answer('Обрабатываю ...')

        checking_for_new_news = search_new_deals()
        if checking_for_new_news == True:
            file = parse_site_xbox_now()

            with open(f'{file}', encoding="utf-8") as parse_result:
                data_file = json.load(parse_result)

            for index, rows in enumerate(data_file):
                print(rows)
                print(f'index is : {index}')
                title = rows.get('game_name')
                img = rows.get('img')
                price = rows.get('price')
                region = rows.get('region')
                url = rows.get('url')
                # f'Регион : <b>{price[0]}</b>\n\n' \
                message = f'Название игры : <b>{title}</b> \n\n' \
                          f'Самая низкая цена : <b>{price}</b> 🔥\n' \
                          f'Регион с такой ценой : <b>{region}</b>\n\n' \
                          f'<a href="{url}">Узнать подробнее о ценах  👀</a>'
                await bot.send_photo(chat_id=xprices_channel, photo=img, caption=message, disable_notification=False)

                if index % 15 == 0:
                    #await bot.send_message(chat_id=xprices_channel, text='Сплю 35 сек')
                    await sleep(40)
    else:
        await message.answer('Я пока не знаю как на это реагировать :(', reply_markup=types.ReplyKeyboardRemove())
