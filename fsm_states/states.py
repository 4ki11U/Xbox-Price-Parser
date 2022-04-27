from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from conductor import dp, bot

from keyboards.inline import inline_keyboards
from keyboards.reply import reply_keyboards
from aiogram import types


class My_State_Machine(StatesGroup):
    Question1 = State()
    Question2 = State()
    Question3 = State()
    Question4 = State()
    Question5 = State()


### ---- Отмена FSM ---- ###
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('FSM-отменён', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=My_State_Machine.Question1)
async def nickname_hero(message: types.message, state: FSMContext):
    answer1 = message.text

    await state.update_data(
        {
            'answer1': f'{answer1}'
        }
    )

    await My_State_Machine.Question2.set()


@dp.message_handler(state=My_State_Machine.Question2)
async def nickname_hero(message: types.message, state: FSMContext):
    answer2 = message.text

    await state.update_data(
        {
            'answer2': f'{answer2}'
        }
    )

    await My_State_Machine.Question3.set()


@dp.message_handler(state=My_State_Machine.Question3)
async def nickname_hero(message: types.message, state: FSMContext):
    answer3 = message.text

    await state.update_data(
        {
            'answer3': f'{answer3}'
        }
    )

    await state.finish()
