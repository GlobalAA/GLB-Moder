from datetime import datetime

from aiogram.types import User

from .models import Penalties, PenaltiesType


class PenaltiesRequests:

	@classmethod
	async def check_penal(cls, penal_type: PenaltiesType, telegram_id: int) -> bool:
		if (user := await Penalties.get_or_none(telegram_id=telegram_id, penalties_type=penal_type)) != None:
			exp = user.expiration
			now = datetime.now(exp.tzinfo)
			if now > exp:
				await user.delete()
				return False
			return True
		return False


	@classmethod
	async def add_penal(cls, penal_type: PenaltiesType, user: User, expiration: datetime) -> bool:
		telegram_id: int = user.id
		username: str | None = user.username
		full_name: str = user.full_name

		is_created = await cls.check_penal(penal_type, telegram_id)

		if not is_created:
			await Penalties.create(telegram_id=telegram_id, username=username, full_name=full_name, penalties_type=penal_type, expiration=expiration)
			return True
		
		return False
	
	@classmethod
	async def remove_penal(cls, penal_type: PenaltiesType, telegram_id: int):
		is_created = await cls.check_penal(penal_type, telegram_id)

		if not is_created:
			return False
		
		if user := await Penalties.get(telegram_id=telegram_id, penalties_type=penal_type):
			await user.delete()
			return True
		
		return False