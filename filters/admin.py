from aiogram import Bot
from aiogram.filters import Filter
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner, Message


class IsAdmin(Filter):
	def __init__(self) -> None:
		super().__init__()
	
	async def __call__(self, message: Message, bot: Bot) -> bool:
		user = await bot.get_chat_member(message.chat.id, message.from_user.id)
		if not user:
			return False
		
		return isinstance(user, ChatMemberAdministrator) or isinstance(user, ChatMemberOwner)