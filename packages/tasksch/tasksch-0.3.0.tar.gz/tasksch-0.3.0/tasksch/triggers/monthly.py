import typing as t
from .base import TaskTrigger
from ..duration import Duration
from ..com import ComField, DurationField
from ..errors import TaskSchdError
from .const import months
from .const.days import DAYS_OF_MONTH
from .descriptors import BitwiseField


class MonthlyTrigger(TaskTrigger):
    """
    IMonthlyTrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-imonthlytrigger

    """

    days_of_month: int = ComField("DaysOfMonth")
    months_of_year: int = ComField("MonthsOfYear")
    random_delay: Duration = DurationField("RandomDelay")
    run_on_last_day_of_month: bool = ComField("RunOnLastDayOfMonth")

    january: bool = BitwiseField("MonthsOfYear", months.JAN)
    february: bool = BitwiseField("MonthsOfYear", months.FEB)
    march: bool = BitwiseField("MonthsOfYear", months.MAR)
    april: bool = BitwiseField("MonthsOfYear", months.APR)
    may: bool = BitwiseField("MonthsOfYear", months.MAY)
    june: bool = BitwiseField("MonthsOfYear", months.JUN)
    july: bool = BitwiseField("MonthsOfYear", months.JUL)
    august: bool = BitwiseField("MonthsOfYear", months.AUG)
    september: bool = BitwiseField("MonthsOfYear", months.SEP)
    october: bool = BitwiseField("MonthsOfYear", months.OCT)
    november: bool = BitwiseField("MonthsOfYear", months.NOV)
    december: bool = BitwiseField("MonthsOfYear", months.DEC)

    def clear_months(self):
        self.months_of_year = 0

    def add_days(self, *days: t.Tuple[int, ...]):
        added_days = 0
        for day in days:
            if day < 1 or day > 31:
                raise TaskSchdError(f"Day {day} is not a valid date.")
            added_days = added_days | DAYS_OF_MONTH.get(day, 0)
        self.days_of_month = self.days_of_month | added_days

    def remove_days(self, *days: t.Tuple[int, ...]):
        days_of_month = 0
        for day in days:
            if day < 1 or day > 31:
                raise TaskSchdError(f"Day {day} is not a valid day.")
            days_of_month = days_of_month ^ DAYS_OF_MONTH.get(day, 0)
        self.days_of_month = self.days_of_month ^ days_of_month

    def day_selected(self, day: int) -> bool:
        day_value = DAYS_OF_MONTH.get(day)
        if day_value is None:
            raise TaskSchdError(f"Day {day} is not a valid day.")
        return bool(self.days_of_month & day_value)
