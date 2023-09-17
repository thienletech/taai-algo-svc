from datetime import datetime, timedelta


def get_date_range(offset_before, offset_after):
    today = datetime.today()
    prev_date = today - timedelta(days=offset_before)
    next_day = today + timedelta(days=offset_after)
    return prev_date, next_day


def format_date(date, format):
    return date.strftime(format)
