from datetime import datetime
from ..com import ComObject, ComField, DateTimeField, EnumField
from enum import Enum


class TriggerType(Enum):
    TASK_TRIGGER_EVENT = 0
    TASK_TRIGGER_TIME = 1
    TASK_TRIGGER_DAILY = 2
    TASK_TRIGGER_WEEKLY = 3
    TASK_TRIGGER_MONTHLY = 4
    TASK_TRIGGER_MONTHLYDOW = 5
    TASK_TRIGGER_IDLE = 6
    TASK_TRIGGER_REGISTRATION = 7
    TASK_TRIGGER_BOOT = 8
    TASK_TRIGGER_LOGON = 9
    TASK_TRIGGER_SESSION_STATE_CHANGE = 11
    TASK_TRIGGER_CUSTOM_TRIGGER_01 = 12


class RepetitionPattern(ComObject):
    """
    IRepetitionPattern: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-irepetitionpattern

    """

    duration: str = ComField("Duration")
    interval: str = ComField("Interval")
    stop_at_duration_end: bool = ComField("StopAtDurationEnd")

    def display(self):
        return ", ".join(
            [
                f"duration: {self.duration}",
                f"interval: {self.interval}",
                f"stop_at_duration_end: {self.stop_at_duration_end}",
            ]
        )


class TaskTrigger(ComObject):
    """
    ITrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itrigger

    """

    id: str = ComField("Id")
    type: TriggerType = EnumField("Type", TriggerType)
    enabled: bool = ComField("Enabled")
    start_boundary: datetime = DateTimeField("StartBoundary")
    end_boundary: datetime = DateTimeField("EndBoundary")
    execution_time_limit: str = ComField("ExecutionTimeLimit")
    repetition: RepetitionPattern = ComField("Repetition", RepetitionPattern)

    def display(self):
        return [
            ("", "TRIGGER"),
            ("id", self.id),
            ("type", self.type),
            ("enabled", self.enabled),
            ("start boundary", self.start_boundary),
            ("end boundary", self.end_boundary),
            ("execute time limit", self.execution_time_limit),
            ("repetition", self.repetition.display()),
        ]
