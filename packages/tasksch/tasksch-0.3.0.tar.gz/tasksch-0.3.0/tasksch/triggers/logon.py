from .base import TaskTrigger
from ..com import Duration, ComField, DurationField


class LogonTrigger(TaskTrigger):
    """
    ILogonTrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-ilogontrigger

    """

    delay: Duration = DurationField("Delay")
    user_id: str = ComField("UserId")
