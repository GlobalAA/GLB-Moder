from aiogram import F
from aiogram.types import Message

from . import event


@event.message(F.new_chat_members)
@event.message(F.new_chat_photo)
@event.message(F.left_chat_member)
@event.message(F.new_chat_title)
@event.message(F.delete_chat_photo)
@event.message(F.pinned_message)
async def main_event(message: Message):
	await message.delete()
