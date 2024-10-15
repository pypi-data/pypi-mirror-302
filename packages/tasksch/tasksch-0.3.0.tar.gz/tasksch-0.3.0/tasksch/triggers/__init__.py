import typing as t
import warnings
from ..com import ComObject
from ..com import ComField
from .base import TaskTrigger
from .base import TriggerType
from .base import RepetitionPattern  # noqa

from .daily import DailyTrigger
from .weekly import WeeklyTrigger
from .monthly import MonthlyTrigger
from .logon import LogonTrigger
from .time import TimeTrigger
from .monthlydow import MonthlyDOWTrigger


TriggerTypeFactory = {
    # on a schedule triggers
    TriggerType.TASK_TRIGGER_TIME: TimeTrigger,
    TriggerType.TASK_TRIGGER_DAILY: DailyTrigger,
    TriggerType.TASK_TRIGGER_WEEKLY: WeeklyTrigger,
    TriggerType.TASK_TRIGGER_MONTHLY: MonthlyTrigger,
    TriggerType.TASK_TRIGGER_MONTHLYDOW: MonthlyDOWTrigger,
    TriggerType.TASK_TRIGGER_LOGON: LogonTrigger,
    # TODO: these remaining types currently have less practical value to
    #   the author and may or may not be implemented unless
    #   the need arises or some enterprising individual
    #   contributes to the project
    TriggerType.TASK_TRIGGER_BOOT: None,
    TriggerType.TASK_TRIGGER_CUSTOM_TRIGGER_01: None,
    TriggerType.TASK_TRIGGER_EVENT: None,
    TriggerType.TASK_TRIGGER_IDLE: None,
    TriggerType.TASK_TRIGGER_REGISTRATION: None,
    TriggerType.TASK_TRIGGER_SESSION_STATE_CHANGE: None,
}


def get_trigger_type_class(trigger_type: TriggerType):
    trigger_class = TriggerTypeFactory.get(trigger_type)
    if not trigger_class:
        trigger_class = TaskTrigger
        warnings.warn(
            f"TriggerType {trigger_type.name} has no implementation. Returning base TaskTrigger type.",
            warnings.WarningMessage,
        )
    return trigger_class


class TaskTriggerCollection(ComObject):
    """
    ITriggerCollection: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itriggercollection

    """

    count: int = ComField("Count")

    def create_trigger(self, trigger_type: TriggerType) -> TaskTrigger:
        trigger_class = get_trigger_type_class(trigger_type)
        return trigger_class(self.com_object.Create(trigger_type.value))

    def create_daily_trigger(self) -> DailyTrigger:
        return DailyTrigger(
            self.com_object.Create(TriggerType.TASK_TRIGGER_DAILY.value)
        )

    def __iter__(self) -> t.Generator[TaskTrigger, t.Any, t.Any]:
        for trigger in self.com_object:
            trigger_class = get_trigger_type_class(TriggerType(trigger.Type))
            yield trigger_class(trigger)
