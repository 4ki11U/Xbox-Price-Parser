from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from keyboards.inline import inline_keyboards
from keyboards.reply import reply_keyboards
from aiogram import types
from conductor import dp
import re

from database_files.X_Database import XboxDB
xboxer = XboxDB(r'database_files\xboxer_database.db')



store_regions = xboxer.select_store_regions()
store_regions_list = []

for region in range(len(store_regions)):
    clear_region = re.sub(r"[(',)]", "", str(store_regions[region]))
    store_regions_list.append(clear_region)


def region_deteils(country):
    region_details = xboxer.select_details_regions(country)
    message = f'<b>{country}</b> : \n\nАдрес - {region_details[0][0]}' \
              f'\nГород - {region_details[0][1]}' \
              f'\nОбласть - {region_details[0][2]}' \
              f'\nПочтовый индекс - {region_details[0][3]}'
    return message


# @dp.callback_query_handler(text=store_regions_list)
@dp.callback_query_handler()
async def kind_race_callbacks_num(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if call.data == '🇦🇷 Аргентина':
        await call.answer()
        await call.message.edit_text(text=region_deteils(call.data), reply_markup=inline_keyboards.inline_back_kb)
    elif call.data == '🇹🇷 Турция':
        await call.answer()
        await call.message.edit_text(text=region_deteils(call.data), reply_markup=inline_keyboards.inline_back_kb)
    elif call.data == '🇮🇳 Индия':
        await call.answer()
        await call.message.edit_text(text=region_deteils(call.data), reply_markup=inline_keyboards.inline_back_kb)
    elif call.data == 'back':
        await call.answer()
        await call.message.edit_text('Выбери регион ниже 👇', reply_markup=inline_keyboards.inline_region_kb())
