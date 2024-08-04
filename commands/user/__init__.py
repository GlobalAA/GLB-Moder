from aiogram import Router

user_commands = Router(name="user_commands")

from .report import report_command
