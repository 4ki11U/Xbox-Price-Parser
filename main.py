from handlers.commands.set_bot_commands import set_default_commands
import handlers, fsm_states, keyboards, systems
from conductor import dp, bot, config
from aiogram.utils import executor


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await bot.send_message(config.my_own_id, text=' /start ')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
