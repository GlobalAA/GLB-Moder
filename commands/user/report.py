from aiogram import Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import OWNER_ID
from interfaces.report import ReportAction, ReportType

from . import user_commands


@user_commands.message(Command("report"))
async def report_command(message: Message, command: CommandObject, bot: Bot):
	reply = message.reply_to_message

	if not reply:
		return await message.reply("Эта команда должна быть ответом на сообщение!")
	
	if reply.from_user.is_bot:
		return await message.reply("Вы не можете отправить жалобу на бота!")
	
	if reply.from_user.id == message.from_user.id:
		return await message.reply("Вы не можете отправить жалобу на самого себя!")

	if reply.from_user.id == OWNER_ID:
		return await message.reply("Вы не можете отправить жалобу на администратора канала!")
	
	reply_message_user_id = reply.from_user.id
	reason = command.args

	if len(reason.strip()) <= 0:
		return await message.reply("У вашей жалобы должна быть причина!")
	
	report_message = f""" 
User id: {reply_message_user_id}
Username: {reply.from_user.username or 'отсутствует'}
Firstname: {reply.from_user.first_name or 'отсутствует'}
Lastname: {reply.from_user.last_name or 'отсутствует'}
Reason for the report: {reason}

From username: {message.from_user.username or 'отсутствует'}
From firstname: {message.from_user.first_name or 'отсутствует'}
From lastname: {message.from_user.last_name or 'отсутствует'}
	"""
	
	try:
		keyboard_builder = InlineKeyboardBuilder()
		keyboard_builder.button(
			text="✅",
			callback_data=ReportAction(report_type=ReportType.approval, id=reply_message_user_id, name=reply.from_user.username or reply.from_user.full_name)
		)
		keyboard_builder.button(
			text="❌", 
			callback_data=ReportAction(report_type=ReportType.discard, id=0, name="")
		)
		keyboard_builder.adjust(2)

		await bot.send_message(OWNER_ID, report_message, reply_markup=keyboard_builder.as_markup())

	except Exception as e:
		raise(e)

	await message.answer(f"Жалоба на пользователя {reply.from_user.full_name} отправлена")
	await message.delete()