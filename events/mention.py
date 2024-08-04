from aiogram import F
from aiogram.types import Message

from . import event


@event.message(F.mention)
async def mention(message: Message):
	await message.delete()