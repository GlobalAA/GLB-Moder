from enum import Enum

from aiogram.filters.callback_data import CallbackData


class ReportType(str, Enum):
	approval = "approval"
	discard = "discard"

class ReportAction(CallbackData, prefix="ra"):
	report_type: ReportType
	id: int
	name: str