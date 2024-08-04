from aiogram.filters import Filter
from aiogram.types import Message


class IsLink(Filter):
	def __init__(self) -> None:
		super().__init__()
	
	async def __call__(self, message: Message) -> bool:
		if (entities := message.entities):
			urls = [entity for entity in entities if entity.type == "url"]
			return len(urls) > 0