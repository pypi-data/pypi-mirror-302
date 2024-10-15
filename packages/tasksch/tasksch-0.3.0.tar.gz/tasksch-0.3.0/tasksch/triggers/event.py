from .base import TaskTrigger
# from ..duration import Duration
# from ..com import DurationField


class EventTrigger(TaskTrigger):
    """
    IEventTrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-ieventtrigger

    """

    # TODO: this requires an indepth study of subscription and value queries
    # delay: Duration = DurationField("Delay")
    # subscription: ???
    # value_queries: ???
