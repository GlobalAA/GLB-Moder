from .admin import admin_commands
from .routers import commands
from .user import user_commands

commands.include_router(user_commands)
commands.include_router(admin_commands)