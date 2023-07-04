from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import html
import requests
from bs4 import BeautifulSoup

from apps.comtrade.models import SkipDay


def get_report_data_using_skip_value() -> str:
    """
    Function process months skip to get report data from comtrade
    @return: last Year and Month of report like: "202205" (May 2022)
    @rtype: str
    """

    # Get current datetime
    current_date = datetime.now()

    # Load days to skip model
    skip_days = SkipDay.load()

    # Subtract specified days from current date
    new_date = current_date - timedelta(days=skip_days.amount)

    # Subtract one month from new date
    previous_month = new_date - relativedelta(months=1)

    # Extract year and month from date
    year = previous_month.year
    month = str(previous_month.month).zfill(2)

    # Create string in comtrade format for request
    last_month_of_report = f"{year}{month}"
    return last_month_of_report
