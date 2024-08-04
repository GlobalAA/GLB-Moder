import logging
from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import Tortoise

from callbacks import callback
from commands import commands
from config import *
from events import event

logging.basicConfig(level=logging.INFO)

bot = Bot(
	BOT_TOKEN,
	default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

async def tortoise_init():
	await Tortoise.init(
		db_url="sqlite://db.sqlite3",
		modules={'models': ['database.models']}
	)

	await Tortoise.generate_schemas()

@dp.startup()
async def on_startup():
	await tortoise_init()
	await bot.delete_webhook(drop_pending_updates=True)

@dp.shutdown()
async def on_shutdown():
	await Tortoise.close_connections()

async def main():
	dp.include_router(event)
	dp.include_router(commands)
	dp.include_router(callback)
	await dp.start_polling(bot)

if __name__ == "__main__":
	run(main())  