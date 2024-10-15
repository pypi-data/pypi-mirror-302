from .base import TaskTrigger
from ..duration import Duration
from ..com import ComField, DurationField


class DailyTrigger(TaskTrigger):
    """
    IDailyTrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-idailytrigger

    """

    days_interval: int = ComField("DaysInterval", int)
    random_delay: Duration = DurationField("RandomDelay")
