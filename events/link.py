from aiogram.types import Message

from filters import IsLink

from . import event


@event.message(IsLink())
async def bad_link(message: Message):
	await message.delete()