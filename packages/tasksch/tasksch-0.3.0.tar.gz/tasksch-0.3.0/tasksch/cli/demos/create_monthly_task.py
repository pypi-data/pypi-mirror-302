from datetime import datetime, timedelta
from tasksch import (
    TaskService,
    TaskFolder,
    TaskDefinition,
    TriggerType,
    Duration,
)
from tasksch.triggers import MonthlyTrigger
from tasksch.validate import validate
from ..utils import console
from .shared import DemoArgs
from . import shared


def set_monthly_schedule_trigger(task: TaskDefinition):
    trigger: MonthlyTrigger = task.triggers.create_trigger(
        TriggerType.TASK_TRIGGER_MONTHLY
    )

    trigger.clear_months()
    trigger.november = True
    trigger.december = True

    trigger.add_days(1, 10, 14, 20)

    trigger.execution_time_limit = Duration(minutes=1)
    execution_time = datetime.now() + timedelta(minutes=5)
    trigger.start_boundary = execution_time
    trigger.enabled = True
    trigger.repetition.duration = Duration(hours=1)
    trigger.repetition.interval = Duration(minutes=1)
    trigger.repetition.stop_at_duration_end = True


def main(ts: TaskService, demo_folder: TaskFolder, args: DemoArgs):
    """
    Monthly Task Demo
    -----------------

    Create a scheduled monthly task that triggers once a month
    and writes to the demo log file.

    """
    task_name = "MONTHLY-DEMO"
    if args.suffix:
        task_name = task_name + "-" + args.suffix

    # check the task exists
    registered_task = demo_folder.find_task(task_name)
    if registered_task and not args.refresh:
        console.print(
            f"     {task_name} task already exists! Exiting without creating task."
        )
        return

    if registered_task and args.refresh:
        demo_folder.delete_task(task_name)

    console.print("[yellow]DEMO[/yellow] Creat Weekly Executing Task")
    task = ts.new_task()
    shared.set_task_registration(task, args.current_user, task_name)
    shared.set_task_exec_action(task, args.current_user, task_name)
    shared.set_task_settings(task)
    shared.set_task_principal(task, args.current_user, args)
    set_monthly_schedule_trigger(task)

    validate(task)

    demo_folder.register_new_task_definition(
        task, task_name, args.current_user.uid, args.current_user.password
    )

    console.print(f"     {task_name} task has been created!")
