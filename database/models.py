from enum import Enum

from tortoise import Model, fields


class PenaltiesType(str, Enum):
	BAN = "ban"
	MUTE = "mute"

class Penalties(Model):
	id = fields.IntField(primary_key=True)
	telegram_id = fields.IntField(primary_key=False)
	username = fields.CharField(max_length=155, null=True, default=None)
	full_name = fields.CharField(max_length=255)
	penalties_type = fields.CharEnumField(enum_type=PenaltiesType)
	expiration = fields.DatetimeField()
	created_at = fields.DatetimeField(auto_now_add=True)

	class Meta:
		table="Наказания"