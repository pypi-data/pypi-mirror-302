from datetime import datetime, timedelta
from tasksch import (
    TaskService,
    TaskFolder,
    TaskDefinition,
    TriggerType,
    Duration,
)
from tasksch.triggers import TimeTrigger
from ..utils import console
from .shared import DemoArgs
from . import shared


def set_time_schedule_trigger(task: TaskDefinition):
    trigger: TimeTrigger = task.triggers.create_trigger(TriggerType.TASK_TRIGGER_TIME)
    trigger.execution_time_limit = Duration(minutes=1)
    execution_time = datetime.now() + timedelta(minutes=5)
    trigger.start_boundary = execution_time
    trigger.end_boundary = execution_time
    # TODO: must supply end_boundary , if we have selected task for deletion...
    # trigger.end_boundary =  None  # EMPTY_DATETIME
    trigger.enabled = True


def main(ts: TaskService, demo_folder: TaskFolder, args: DemoArgs):
    """
    Time Task Demo
    --------------

    Create a scheduled time task that triggers 5 minutes after its
    been created, and writes to the demo log file.

    """
    task_name = "TIME-DEMO"
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

    console.print("[yellow]DEMO[/yellow] Creat Timed Task")
    task = ts.new_task()
    shared.set_task_registration(task, args.current_user, task_name)
    shared.set_task_exec_action(task, args.current_user, task_name)
    shared.set_task_settings(task)
    shared.set_task_principal(task, args.current_user, args)
    set_time_schedule_trigger(task)

    demo_folder.register_new_task_definition(
        task, task_name, args.current_user.uid, args.current_user.password
    )

    console.print(f"     {task_name} task has been created!")
