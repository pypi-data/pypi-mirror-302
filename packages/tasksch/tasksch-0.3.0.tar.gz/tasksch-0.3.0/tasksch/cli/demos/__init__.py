from tasksch import TaskService
from .shared import DEMO_FOLDER_NAME, CurrentUser, DemoArgs
from . import create_demo_folder
from . import create_time_task
from . import create_daily_task
from . import create_weekly_task
from . import create_monthly_task
from . import create_monthlydow_task


def demo_command(args: DemoArgs):
    current_user = CurrentUser()
    current_user.ask_password()

    args.current_user = current_user

    with TaskService() as ts:
        create_demo_folder.main(ts)
        demo_folder = ts.root_folder().get_folder(DEMO_FOLDER_NAME)

        if args.delete_all:
            for task in demo_folder.tasks(include_hidden=True):
                demo_folder.delete_task(task.name)

        if args.time_trigger:
            create_time_task.main(ts, demo_folder, args)

        if args.daily_trigger:
            create_daily_task.main(ts, demo_folder, args)

        if args.weekly_trigger:
            create_weekly_task.main(ts, demo_folder, args)

        if args.monthly_trigger:
            create_monthly_task.main(ts, demo_folder, args)

        if args.monthlydow_trigger:
            create_monthlydow_task.main(ts, demo_folder, args)
