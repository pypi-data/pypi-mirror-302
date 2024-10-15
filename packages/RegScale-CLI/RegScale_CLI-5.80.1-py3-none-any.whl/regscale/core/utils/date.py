#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Utility functions for handling date and datetime conversions """

import datetime
import logging
from typing import List, Union, Optional

from dateutil.parser import parse, ParserError


logger = logging.getLogger("rich")
default_date_format = "%Y-%m-%dT%H:%M:%S%z"


def date_str(date_object: Union[str, datetime.datetime, datetime.date, None], date_format: Optional[str] = None) -> str:
    """
    Convert a date/datetime object to a date string.

    :param Union[str, datetime.datetime, datetime.date, None] date_object: The date/datetime object to convert.
    :param Optional[str] date_format: The format to use for the date string.
    :return: The date as a string.
    """
    if isinstance(date_object, str):
        date_object = date_obj(date_object)
    if isinstance(date_object, datetime.datetime):
        if date_format:
            return date_object.strftime(date_format)
        return date_object.date().isoformat()
    if isinstance(date_object, datetime.date):
        if date_format:
            return date_object.strftime(date_format)
        return date_object.isoformat()
    return ""


def datetime_str(
    date_object: Union[str, datetime.datetime, datetime.date, None], date_format: Optional[str] = None
) -> str:
    """
    Convert a date/datetime object to a datetime string.

    :param Union[str, datetime.datetime, datetime.date, None] date_object: The date/datetime object to convert.
    :param Optional[str] date_format: The format to use for the datetime string.
    :return: The datetime as a string.
    """
    if not date_format:
        date_format = default_date_format
    if isinstance(date_object, str):
        date_object = datetime_obj(date_object)
    if isinstance(date_object, datetime.datetime):
        return date_object.strftime(date_format)
    if isinstance(date_object, datetime.date):
        return date_object.strftime(date_format)
    return ""


def date_obj(date_str: Union[str, datetime.datetime, datetime.date, int, None]) -> Optional[datetime.date]:
    """
    Convert a string, datetime, date, or integer to a date object.

    :param Union[str, datetime.datetime, datetime.date, int] date_str: The value to convert.
    :return: The date object.
    """
    if isinstance(date_str, (str, int)):
        dt_obj = datetime_obj(date_str)
        return dt_obj.date() if dt_obj else None
    if isinstance(date_str, datetime.datetime):
        return date_str.date()
    if isinstance(date_str, datetime.date):
        return date_str
    return None


def datetime_obj(date_str: Union[str, datetime.datetime, datetime.date, int, None]) -> Optional[datetime.datetime]:
    """
    Convert a string, datetime, date, integer, or timestamp string to a datetime object.

    :param Union[str, datetime.datetime, datetime.date, int, None] date_str: The value to convert.
    :return: The datetime object.
    """
    if isinstance(date_str, str):
        # Check if the string looks like a timestamp integer
        if date_str.isdigit():
            return datetime.datetime.fromtimestamp(int(date_str))
        try:
            return parse(date_str)
        except ParserError as e:
            if date_str and str(date_str).lower() not in ["n/a", "none"]:
                logger.warning(f"Warning could not parse date string: {date_str}\n{e}")
            return None
    if isinstance(date_str, datetime.datetime):
        return date_str
    if isinstance(date_str, datetime.date):
        return datetime.datetime.combine(date_str, datetime.datetime.min.time())
    if isinstance(date_str, int):
        return datetime.datetime.fromtimestamp(date_str)
    return None


def time_str(time_obj: Union[str, datetime.datetime, datetime.time]) -> str:
    """
    Convert a datetime/time object to a string.

    :param Union[str, datetime.datetime, datetime.time] time_obj: The datetime/time object to convert.
    :return: The time as a string.
    """
    if isinstance(time_obj, str):
        return time_obj
    if isinstance(time_obj, datetime.datetime):
        time_obj = time_obj.time()
    if isinstance(time_obj, datetime.time):
        return time_obj.__format__("%-I:%M%p")
    return ""


def time_widget_str(time_obj: Union[str, datetime.datetime, datetime.time]) -> str:
    """
    Convert a time object to a string for a widget.

    :param Union[str, datetime.datetime, datetime.time] time_obj: The time object to convert.
    :return: The time as a string for a widget.
    """
    if isinstance(time_obj, str):
        return time_obj
    if isinstance(time_obj, datetime.datetime):
        time_obj = time_obj.time()
    if isinstance(time_obj, datetime.time):
        return time_obj.__format__("%-I:%M ") + time_obj.__format__("%p").lower()
    return ""


def parse_time(time_str: str) -> datetime.time:
    """
    Parse a time string.

    :param str time_str: The time string to parse.
    :return: The parsed time.
    :rtype: datetime.time
    """
    try:
        return parse(f"1/1/2011 {time_str.zfill(4)}").time()
    except ValueError:
        return parse(f"1/1/2011 {time_str.zfill(len(time_str) + 1)}").time()


def is_weekday(date_obj: datetime.date) -> bool:
    """
    Check if a date is a weekday.

    :param datetime.date date_obj: The date to check.
    :return: True if the date is a weekday, False otherwise.
    :rtype: bool
    """
    return date_obj.weekday() < 5


def days_between(
    start: Union[str, datetime.datetime, datetime.date],
    end: Union[str, datetime.datetime, datetime.date],
) -> List[str]:
    """
    Get the days between two dates.

    :param Union[str, datetime.datetime, datetime.date] start: The start date.
    :param Union[str, datetime.datetime, datetime.date] end: The end date.
    :return: A list of dates between the start and end dates.
    """
    delta = date_obj(end) - date_obj(start)
    return [(date_obj(start) + datetime.timedelta(days=i)).strftime("%Y/%m/%d") for i in range(delta.days + 1)]


def weekend_days_between(
    start: Union[str, datetime.datetime, datetime.date],
    end: Union[str, datetime.datetime, datetime.date],
) -> List[str]:
    """
    Get the weekend days between two dates.

    :param Union[str, datetime.datetime, datetime.date] start: The start date.
    :param Union[str, datetime.datetime, datetime.date] end: The end date.
    :return: A list of weekend dates between the start and end dates.
    """
    return [day for day in days_between(start, end) if not is_weekday(date_obj(day))]


def days_from_today(i: int) -> datetime.date:
    """
    Get the date a certain number of days from today.

    :param int i: The number of days from today.
    :return: The date i days from today.
    :rtype: datetime.date
    """
    return datetime.date.today() + datetime.timedelta(days=i)


def get_day_increment(
    start: Union[str, datetime.datetime, datetime.date],
    days: int,
    excluded_dates: Optional[List[Union[str, datetime.datetime, datetime.date]]] = None,
) -> datetime.date:
    """
    Get the date a certain number of days from a start date, excluding certain dates.

    :param Union[str, datetime.datetime, datetime.date] start: The start date.
    :param int days: The number of days from the start date.
    :param Optional[List[Union[str, datetime.datetime, datetime.date]]] excluded_dates: A list of dates to exclude.
    :return: The date days days from the start date, excluding the excluded dates.
    """
    start = date_obj(start)
    end = start + datetime.timedelta(days=days)
    if excluded_dates:
        for excluded_date in sorted([date_obj(x) for x in excluded_dates]):
            if start <= excluded_date <= end:
                end += datetime.timedelta(days=1)
    return end


def normalize_date(dt: str, fmt: str) -> str:
    """
    Normalize string date to a standard format, if possible.

    :param str dt: Date to normalize
    :param str fmt: Format of the date
    :return: Normalized Date
    :rtype: str
    """
    if isinstance(dt, str):
        try:
            new_dt = datetime.datetime.strptime(dt, fmt)
            return new_dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return dt
    return dt
