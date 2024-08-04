from aiogram import Bot, F
from aiogram.types import CallbackQuery

from config import CHAT_ID
from interfaces.report import ReportAction, ReportType

from . import callback


@callback.callback_query(ReportAction.filter(F.report_type == ReportType.approval))
async def approval_report(call: CallbackQuery, callback_data: ReportAction, bot: Bot):
	await bot.ban_chat_member(CHAT_ID, callback_data.id)
	await call.answer(text="Жалоба обработана", show_alert=True, cache_time=2)
	await call.message.delete()
	await bot.send_message(CHAT_ID, f"{callback_data.name} был исключен администратором")

@callback.callback_query(ReportAction.filter(F.report_type == ReportType.discard))
async def discard_report(call: CallbackQuery):
	await call.answer(text="Жалоба отклонена", show_alert=True, cache_time=2)
	await call.message.delete()