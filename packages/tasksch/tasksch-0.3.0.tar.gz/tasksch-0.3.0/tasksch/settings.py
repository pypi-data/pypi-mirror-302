from .com import ComObject, ComField, EnumField, DurationField
from enum import Enum


class TaskCompatibility(Enum):
    """
    TASK_COMPATIBILITY: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_compatibility

    """

    TASK_COMPATIBILITY_AT = 0
    TASK_COMPATIBILITY_V1 = 1
    TASK_COMPATIBILITY_V2 = 2
    TASK_COMPATIBILITY_V2_1 = 3
    TASK_COMPATIBILITY_V2_2 = 4
    TASK_COMPATIBILITY_V2_3 = 5
    TASK_COMPATIBILITY_V2_4 = 6


class TaskInstancesPolicy(Enum):
    """
    TASK_INSTANCES_POLICY: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_instances_policy

    """

    TASK_INSTANCES_PARALLEL = 0
    TASK_INSTANCES_QUEUE = 1
    TASK_INSTANCES_IGNORE_NEW = 2
    TASK_INSTANCES_STOP_EXISTING = 3


class TaskSettings(ComObject):
    """
    ITaskSettings: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itasksettings

    """

    allow_demand_start: bool = ComField("AllowDemandStart")
    allow_hard_terminate: bool = ComField("AllowHardTerminate")
    compatibility: TaskCompatibility = EnumField("Compatibility", TaskCompatibility)
    delete_expired_task_after: str = DurationField("DeleteExpiredTaskAfter")
    disallow_start_if_on_batteries: bool = ComField("DisallowStartIfOnBatteries")
    enabled: bool = ComField("Enabled")
    execution_time_limit: str = DurationField("ExecutionTimeLimit")
    hidden: bool = ComField("Hidden")
    # idle_settings: str = ComField("IdleSettings")
    multiple_instances: TaskInstancesPolicy = EnumField(
        "MultipleInstances", TaskInstancesPolicy
    )
    # network_settings: bool = ComField("NetworkSettings")
    priority: int = ComField("Priority")
    restart_count: int = ComField("RestartCount")
    restart_interval: str = ComField("RestartInterval")
    run_only_if_idle: bool = ComField("RunOnlyIfIdle")
    run_only_if_network_available: bool = ComField("RunOnlyIfNetworkAvailable")
    start_when_available: bool = ComField("StartWhenAvailable")
    stop_if_going_on_batteries: bool = ComField("StopIfGoingOnBatteries")
    wake_to_run: bool = ComField("WakeToRun")
    xml_text: str = ComField("XmlText")

    # def xml_text(self) -> str:
    #     return self.com_object.XmlText()
