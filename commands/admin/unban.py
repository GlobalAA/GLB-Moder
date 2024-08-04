from aiogram import Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from database.requests import PenaltiesRequests, PenaltiesType
from filters import ChatType

from . import admin_commands


@admin_commands.message(ChatType(["group", "supergroup"]), Command("unban"))
async def unban_command(message: Message, command: CommandObject, bot: Bot):
	args = command.args.strip()

	if not args:
		return await message.reply("Укажите id пользователя")
	

	if not await bot.get_chat_member(message.chat.id, args):
		return await message.reply("Пользователь не найден")
	
	is_banned = await PenaltiesRequests.check_penal(PenaltiesType.BAN, args)

	if is_banned:
		if await PenaltiesRequests.remove_penal(PenaltiesType.BAN, args):
			await bot.unban_chat_member(message.chat.id, args, True)
			return await message.reply("Пользователь успешно разблокирован!")
		
		return await message.reply("Произошла ошибка")


	return await message.reply("Пользователь не заблокирован")