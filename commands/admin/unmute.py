from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import ChatPermissions, Message

from database.requests import PenaltiesRequests, PenaltiesType
from filters import ChatType
from utils.is_member import check_chat_member

from . import admin_commands


@admin_commands.message(ChatType(["group", "supergroup"]), Command("unmute"))
async def unmute_command(message: Message, bot: Bot):
	if not message.reply_to_message:
		return await message.reply("Ета команда должна быть ответом на сообщение")
	
	reply = message.reply_to_message
	
	user = await bot.get_chat_member(message.chat.id, reply.from_user.id)

	if not check_chat_member(user):
		return await message.reply("Пользователь не найден!")

	is_muted = await PenaltiesRequests.check_penal(PenaltiesType.MUTE, reply.from_user.id)

	if not is_muted:
		return await message.reply("Пользователь не заглушен!")

	if not await PenaltiesRequests.remove_penal(PenaltiesType.MUTE, reply.from_user.id):
		return await message.reply("Произошла ошибка...")

	await bot.restrict_chat_member(
		message.chat.id, 
		reply.from_user.id,
		permissions=ChatPermissions(
			can_send_messages=True,
			can_send_polls=True,
			can_send_other_messages=True,
			can_send_media_messages=True
		)
	)

	await reply.reply("Пользователю успешно было выдано право писать!")
	await message.delete()
