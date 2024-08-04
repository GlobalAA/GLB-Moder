from aiogram.types import ChatMemberBanned, ChatMemberLeft, ChatMemberMember


def check_chat_member(user):
	if (data := isinstance(user, ChatMemberBanned | ChatMemberLeft)):
		return data
	elif (data := isinstance(user, ChatMemberMember)):
		return data
	elif not user.is_member:
		return False
	else:
		return True