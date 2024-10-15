from .base import TaskTrigger
from ..duration import Duration
from ..com import ComField, DurationField
from .const import days
from .descriptors import BitwiseField


class WeeklyTrigger(TaskTrigger):
    """
    IWeeklyTrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-iweeklytrigger

    """

    days_of_week: int = ComField("DaysOfWeek")
    random_delay: Duration = DurationField("RandomDelay")
    weeks_interval: int = ComField("WeeksInterval")

    monday: bool = BitwiseField("DaysOfWeek", days.MON)
    tuesday: bool = BitwiseField("DaysOfWeek", days.TUE)
    wednesday: bool = BitwiseField("DaysOfWeek", days.WED)
    thursday: bool = BitwiseField("DaysOfWeek", days.THU)
    friday: bool = BitwiseField("DaysOfWeek", days.FRI)
    saturday: bool = BitwiseField("DaysOfWeek", days.SAT)
    sunday: bool = BitwiseField("DaysOfWeek", days.SUN)

    @property
    def week_days(self) -> bool:
        return all(
            [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday]
        )

    @week_days.setter
    def week_days(self, value: bool):
        self.monday = value
        self.tuesday = value
        self.wednesday = value
        self.thursday = value
        self.friday = value
