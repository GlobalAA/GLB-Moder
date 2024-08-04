from datetime import UTC, datetime, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from database.requests import PenaltiesRequests, PenaltiesType
from filters import ChatType
from utils.is_member import check_chat_member
from utils.time import convert_to_timedelta

from . import admin_commands


@admin_commands.message(ChatType(["group", "supergroup"]), Command("ban"))
async def ban_command(message: Message, command: CommandObject, bot: Bot):
	reply = message.reply_to_message

	if not reply:
		return await message.reply("Эта команда должна быть ответом на сообщение!")
	
	if reply.from_user.id == message.from_user.id:
		return await message.reply("Вы не можете забанить самого себя")

	is_banned = await PenaltiesRequests.check_penal(PenaltiesType.BAN, reply.from_user.id)

	if is_banned:
		return await message.reply("Пользователь уже заблокирован!")

	user = await bot.get_chat_member(message.chat.id, reply.from_user.id)

	if not check_chat_member(user):
		return await message.reply("Пользователь не найден!")

	if not command.args:
		return await message.reply("Укажите пожалуйста время бана! (/ban 12s)")

	time = convert_to_timedelta(command.args)

	if not time:
		return await message.reply("Неправильный формат!\nДоступные форматы: s, m, h, d")

	expiration = datetime.now(UTC) + time

	if not await PenaltiesRequests.add_penal(PenaltiesType.BAN, reply.from_user, expiration):
		return await message.reply("Произошла ошибка...")

	try:
		await bot.ban_chat_member(message.chat.id, reply.from_user.id, until_date=expiration)
		await message.answer(f"Пользователь {reply.from_user.username or reply.from_user.full_name} был заблокирован администратором!")
		await message.delete()
	except TelegramBadRequest:
		await message.reply("Произошла ошибка, скорее всего, вы не можете выгнать данного пользователя")