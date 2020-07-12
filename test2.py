import logging
from aiogram import Bot, Dispatcher, executor, types 

import gettoken

logging.basicConfig(level=logging.INFO)
bot = Bot(token = gettoken.token())
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
