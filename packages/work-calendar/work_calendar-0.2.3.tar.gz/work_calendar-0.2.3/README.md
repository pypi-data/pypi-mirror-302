![PyPI](https://img.shields.io/pypi/v/work-calendar?label=pypi%20work-calendar)
![ruff](https://github.com/Polyrom/work-calendar/actions/workflows/linter.yml/badge.svg) ![tests](https://github.com/Polyrom/work-calendar/actions/workflows/tests.yml/badge.svg)

# WorkCalendar

A simple no-nonsense library to find out whether a day is a working day in Russia.

Data parsed from [consultant.org](https://www.consultant.ru).

Data available **only for years 2015-2025**.

Feel free to use the [raw json file](work_calendar/total.json).

## Installation

```bash
pip install work-calendar
```

## Basic (and only) usage

```
>>> from datetime import date
>>> from work_calendar import WorkCalendar
>>>
>>> dt = date(year=2021, month=1, day=2)
>>> WorkCalendar.is_workday(dt)
False
>>> dt_out_of_bounds = date(year=2027, month=1, day=2)
>>> WorkCalendar.is_day_off(dt_out_of_bounds)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    <...>
    raise exceptions.NoDataForYearError(year)
work_calendar.exceptions.NoDataForYearError: No data found for holidays in year 2027
```
