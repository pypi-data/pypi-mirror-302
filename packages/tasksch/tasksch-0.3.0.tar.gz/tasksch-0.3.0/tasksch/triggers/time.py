from .base import TaskTrigger
from ..duration import Duration
from ..com import DurationField


class TimeTrigger(TaskTrigger):
    """
    ITimeTrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itimetrigger

    """

    random_delay: Duration = DurationField("RandomDelay")
