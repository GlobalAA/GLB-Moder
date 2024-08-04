from datetime import UTC, datetime, timedelta


def convert_to_timedelta(time_str: str) -> timedelta | bool:
	time_units = {
		's': 'seconds',
		'm': 'minutes',
		'h': 'hours',
		'd': 'days'
	}
	
	num = int(time_str[:-1])
	unit = time_str[-1]

	if unit in time_units:
		return timedelta(**{time_units[unit]: num})
	else:
		return False