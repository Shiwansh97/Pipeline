import pandas as pd
from datetime import datetime, timedelta
now = datetime.now()
year = now.year
month_name = now.strftime("%b")  # Jan, Feb, Mar ...

def get_week_of_month(date):
    first_day = date.replace(day=1)
    days_since_monday = first_day.weekday()
    month_week_start = first_day - timedelta(days=days_since_monday)

    date_week_start = date - timedelta(days=date.weekday())
    weeks_diff = (date_week_start - month_week_start).days // 7
    return weeks_diff + 1

current_week = get_week_of_month(now)