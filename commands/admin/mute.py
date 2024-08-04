from datetime import UTC, datetime

from aiogram import Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import ChatPermissions, Message

from database.requests import PenaltiesRequests, PenaltiesType
from filters import ChatType
from utils.is_member import check_chat_member
from utils.time import convert_to_timedelta

from . import admin_commands


@admin_commands.message(ChatType(["group", "supergroup"]), Command("mute"))
async def mute_command(message: Message, command: CommandObject, bot: Bot):
	if not message.reply_to_message:
		return await message.reply("Ета команда должна быть ответом на сообщение")
	
	reply = message.reply_to_message
	
	user = await bot.get_chat_member(message.chat.id, reply.from_user.id)

	if not check_chat_member(user):
		return await message.reply("Пользователь не найден!")

	is_muted = await PenaltiesRequests.check_penal(PenaltiesType.MUTE, reply.from_user.id)

	if is_muted:
		return await message.reply("Пользователь уже заглушен!")

	if not command.args:
		return await message.reply("Укажите пожалуйста время мута! (/mute 12s)")
	
	time = convert_to_timedelta(command.args)

	if not time:
		return await message.reply("Неправильный формат!\nДоступные форматы: s, m, h, d")
	
	expiration = datetime.now(UTC) + time

	if not await PenaltiesRequests.add_penal(PenaltiesType.MUTE, reply.from_user, expiration):
		return await message.reply("Произошла ошибка...")

	await bot.restrict_chat_member(
		message.chat.id, 
		reply.from_user.id,
		until_date=expiration,
		permissions=ChatPermissions(
			can_send_messages=False,
			can_send_polls=False,
			can_send_other_messages=False,
			can_send_media_messages=False
		)
	)

	await message.answer("Пользователь успешно был заглушен!")
	await message.delete()
