from .base import TaskTrigger
from ..duration import Duration
from ..com import ComField, DurationField
from .const import months
from .const import days
from .const import week
from .descriptors import BitwiseField


class MonthlyDOWTrigger(TaskTrigger):
    """
    IMonthlyTrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-imonthlytrigger

    """

    months_of_year: int = ComField("MonthsOfYear")
    days_of_week: int = ComField("DaysOfWeek")
    weeks_of_month: int = ComField("WeeksOfMonth")

    random_delay: Duration = DurationField("RandomDelay")
    run_on_last_day_of_month: bool = ComField("RunOnLastDayOfMonth")

    def clear_months(self):
        self.months_of_year = 0

    # get/set months of year
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

    def clear_dow(self):
        self.days_of_week = 0

    # get/set days of week
    monday: bool = BitwiseField("DaysOfWeek", days.MON)
    tuesday: bool = BitwiseField("DaysOfWeek", days.TUE)
    wednesday: bool = BitwiseField("DaysOfWeek", days.WED)
    thursday: bool = BitwiseField("DaysOfWeek", days.THU)
    friday: bool = BitwiseField("DaysOfWeek", days.FRI)
    saturday: bool = BitwiseField("DaysOfWeek", days.SAT)
    sunday: bool = BitwiseField("DaysOfWeek", days.SUN)

    def clear_weeks_of_month(self):
        self.weeks_of_month = 0

    # get/set week of month
    first_week: bool = BitwiseField("WeeksOfMonth", week.FIRST)
    second_week: bool = BitwiseField("WeeksOfMonth", week.SECOND)
    third_week: bool = BitwiseField("WeeksOfMonth", week.THIRD)
    fourth_week: bool = BitwiseField("WeeksOfMonth", week.FOURTH)
    last_week: bool = BitwiseField("WeeksOfMonth", week.LAST)
