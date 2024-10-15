from .task import TaskDefinition
from .duration import EMPTY_DURATION
from .com import EMPTY_DATETIME


class TaskValidationError(Exception):
    pass


def flagged_for_deletion(task: TaskDefinition) -> str | None:
    if task.settings.delete_expired_task_after != EMPTY_DURATION:
        for trigger in task.triggers:
            if trigger.end_boundary == EMPTY_DATETIME:
                return "When task is set to delete after expiry, then triggers must provide an end boundary date."


def validate(task: TaskDefinition):
    errors = []
    for validator in (flagged_for_deletion,):
        if err := validator(task):
            errors.append(err)

    if errors:
        err_msg = f"{len(errors)} issues with task definition:\n"
        err_msg = "\n".join(f" > {e}" for e in errors)
        raise TaskValidationError(err_msg)
