from aiogram.utils import exceptions

from config_files.config import xprices_channel
from keyboards.reply import reply_keyboards
from keyboards.inline import inline_keyboards
from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from conductor import dp, bot

from additional.parser import parse_site_xbox_now
from datetime import datetime
import json
from asyncio import sleep


@dp.errors_handler(exception=exceptions.RetryAfter)
@dp.message_handler(Text(equals=['Найти халяву !', 'Адрес регионов', 'Тестовая кнопка']))
async def start(message: types.Message):
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
    elif message.text == 'Тестовая кнопка':
        await message.answer('Обрабатываю ...')

        with open(r'D:\Python Projects\Xboxer-bot\additional\price_30-04-2022.json') as parse_result:
            file_parse = json.load(parse_result)

        count = 0
        try:
            for index, lines in enumerate(file_parse):
                print(lines)
                title = lines.get('game_name')
                url = lines.get('url')
                img = lines.get('img')
                price = lines.get('price')

                message1 = f'Название игры : <b>{title}</b> \n\n'
                message2 = f'Самая низкая цена : <b>{price}</b> 🔥 \n\n'
                message3 = f'<a href="{url}">Узнать подробнее о ценах  👀</a>'
                message = message1 + message2 + message3

                await bot.send_photo(chat_id=xprices_channel, photo=f'{img}', caption=message,
                                     disable_notification=False)
                #count += 1
                print(index)
                if index % 10 == 0:
                    await bot.send_message(chat_id=xprices_channel, text='Сплю 35 сек')
                    await sleep(35)
        except exceptions:
            await bot.send_message(chat_id=xprices_channel, text='Сплю 35 сек')
            await sleep(35)
    else:
        await message.answer('Я пока не знаю как на это реагировать :(', reply_markup=types.ReplyKeyboardRemove())
# result_from_parse = parse_site_xbox_now()
# # print(from_site)
# try:
#     count = 0
#     for index, game_details in enumerate(result_from_parse):
#         title = game_details.get('game_name')
#         url = game_details.get('url')
#         img = game_details.get('img')
#         price = game_details.get('price')
#         # print(game_details.get('game_name'))
#         # print(game_details.get('img'))
#         # print(game_details.get('url'))
#         # print(game_details.get('price'))
#         # print('#' * 15)
#         message1 = f'Название игры : <b>{title}</b> \n\n'
#         message2 = f'Самая низкая цена : <b>{price}</b> 🔥 \n\n'
#         message3 = f'<a href="{url}">Узнать подробнее о ценах  👀</a>'
#         message = message1 + message2 + message3
#         # await bot.send_message(chat_id=xprices_channel, text=message)
#         await bot.send_photo(chat_id=xprices_channel, photo=f'{img}', caption=message,
#                              disable_notification=False)
#
#         count += 1
#         if count == 15:
#             await sleep(10)
# except exceptions :
#     await bot.send_message(chat_id=xprices_channel, text='Сплю 10 сек')
#     await sleep(10)
