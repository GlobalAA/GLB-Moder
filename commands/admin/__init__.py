from aiogram import Router

from filters import IsAdmin

admin_commands = Router(name="admin_commands")
admin_commands.message.filter(IsAdmin())

from .ban import ban_command
from .mute import mute_command
from .unban import unban_command
from .unmute import unmute_command
