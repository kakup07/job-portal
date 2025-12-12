from datetime import datetime
from zoneinfo import ZoneInfo


def get_ist_date(date):
  ts_str = date
  dt_utc = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
  dt_utc = dt_utc.replace(tzinfo=ZoneInfo("UTC"))
  dt_ist = dt_utc.astimezone(ZoneInfo("Asia/Kolkata"))
  return dt_ist