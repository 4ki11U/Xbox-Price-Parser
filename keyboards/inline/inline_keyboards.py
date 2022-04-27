from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
import re

from database_files.X_Database import XboxDB
xboxer = XboxDB(r'database_files\xboxer_database.db')



inline_back_kb = InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton('⬅️ Назад', callback_data='back'))


def inline_region_kb():
    store_regions = xboxer.select_store_regions()
    my_list_for_buttons = []

    for region in range(len(store_regions)):
        clear_region = re.sub(r"[(',)]", "", str(store_regions[region]))
        my_list_for_buttons.append(clear_region)

    button_list = [types.InlineKeyboardButton(text=name, callback_data=name) for name in my_list_for_buttons]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*button_list)

    return keyboard
