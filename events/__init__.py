from aiogram import Router

event = Router(name="event_router")	

from .link import bad_link
from .mention import mention
from .user import main_event
