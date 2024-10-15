import os
import sys
import getpass
import typing as t
from pathlib import Path
from tasksch import TaskService
from tasksch import TaskDefinition
from tasksch import Duration
from tasksch import TaskInstancesPolicy
from tasksch import TaskCompatibility
from tasksch import TaskRunlevelType
from ..utils import console


DEMO_FOLDER_NAME = "TASKSCH-DEMOS"


def create_demo_folder(ts: TaskService) -> bool | None:
    """
    If the folder does not exist, create it and return True.

    Of the folder already exists, return None.


    """
    root = ts.root_folder()
    if not root.has_folder(DEMO_FOLDER_NAME):
        root.create_folder(DEMO_FOLDER_NAME)
        return True


class CurrentUser:
    uid: str
    pwd: str

    def __init__(self):
        domain = os.environ["USERDOMAIN"]
        uid = os.environ["USERNAME"]
        self.uid = f"{domain}\\{uid}"
        self.pwd = ""

    def ask_password(self):
        attempts = 0
        while not self.pwd and attempts < 3:
            attempts += 1
            pwd = getpass.getpass()
            if pwd:
                self.pwd = pwd
                return
        console.debug("Failed to provide a password, exiting program.")
        sys.exit(0)

    @property
    def name(self) -> str:
        return self.uid

    @property
    def password(self) -> str:
        return self.pwd

    @property
    def home(self) -> Path:
        return Path.home()


class DemoExecutable:
    user: CurrentUser

    def __init__(self, user: CurrentUser):
        self.user = user

    @property
    def output_dir(self) -> Path:
        return Path(self.user.home, ".tasksch-demo")

    @property
    def exec_program(self) -> Path:
        return Path(self.output_dir, "tasksch_demo.bat")

    def assert_output_dir(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def assert_exec_program(self) -> str:
        """
        This is a simple batch file program that output to a log:

        echo %DATE% %TIME%: %* >> tasksch_demo_execution_log.txt

        """

        program = "echo %DATE% %TIME%: %* >> tasksch_demo_execution_log.txt"
        if not self.exec_program.exists():
            self.exec_program.write_text(program)


def set_task_registration(task: TaskDefinition, user: CurrentUser, demo_name: str):
    task.registration_info.author = f"tasksch on behalf of {user.name}"
    task.registration_info.description = f"tasksch {demo_name}"


def set_task_exec_action(task: TaskDefinition, user: CurrentUser, demo_name: str):
    exec = DemoExecutable(user)
    exec.assert_output_dir()
    exec.assert_exec_program()

    new_action = task.actions.create_exec_action()
    new_action.path = str(exec.exec_program)
    new_action.working_directory = str(exec.output_dir)
    new_action.arguments = demo_name


def set_task_settings(task: TaskDefinition):
    task.settings.allow_demand_start = True
    task.settings.execution_time_limit = Duration(minutes=1)
    task.settings.hidden = False
    task.settings.multiple_instances = TaskInstancesPolicy.TASK_INSTANCES_IGNORE_NEW
    task.settings.compatibility = TaskCompatibility.TASK_COMPATIBILITY_V2_4
    # task.settings.delete_expired_task_after = Duration(days=5)


def set_task_principal(task: TaskDefinition, user: CurrentUser, args: "DemoArgs"):
    task.principal.user_id = user.name
    task.principal.run_level = TaskRunlevelType.TASK_RUNLEVEL_HIGHEST
    task.principal.state.set_logon_type(
        args.set_logged_in_only, args.set_store_password
    )
    # task.principal.logon_type = TaskLogonType.TASK_LOGON_INTERACTIVE_TOKEN_OR_PASSWORD
    # task.principal.logon_type = TaskLogonType.TASK_LOGON_INTERACTIVE_TOKEN
    # task.principal.logon_type = TaskLogonType.TASK_LOGON_S4U
    # task.principal.logon_type = TaskLogonType.TASK_LOGON_PASSWORD


class DemoArgs(t.Protocol):
    time_trigger: bool
    daily_trigger: bool
    weekly_trigger: bool
    monthly_trigger: bool
    monthlydow_trigger: bool
    delete_all: bool
    refresh: bool
    suffix: str
    current_user: CurrentUser
    set_logged_in_only: bool
    set_store_password: bool
