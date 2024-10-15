from .com import ComObject, ComField, EnumField
from enum import Enum


class TaskLogonType(Enum):
    """
    TASK_LOGON_TYPE: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_logon_type

    The logon type is only valid when there is a Principal.UserId.

    INTERACTIVE_TOKEN = only runs when user is logged in, but sets do not store password

    # run whether user logged in or not:
    INTERACTIVE_TOKEN_OR_PASSWORD = doesn't store password
    S4U = doesn't store password
    PASSWORD = stores password

    # unable to confirm these selections
    NONE = ???
    GROUP = ??? (assume this options is set when group_id populated
    SERVICE_ACCOUNT = ??? (assume this option is set when user_id is service account)
    """

    TASK_LOGON_NONE = 0
    TASK_LOGON_PASSWORD = 1
    TASK_LOGON_S4U = 2
    TASK_LOGON_INTERACTIVE_TOKEN = 3
    TASK_LOGON_GROUP = 4
    TASK_LOGON_SERVICE_ACCOUNT = 5
    TASK_LOGON_INTERACTIVE_TOKEN_OR_PASSWORD = 6


class TaskRunlevelType(Enum):
    """
    TASK_RUNLEVEL_TYPE: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_runlevel_type

    """

    TASK_RUNLEVEL_LUA = 0
    TASK_RUNLEVEL_HIGHEST = 1


class Principle(ComObject):
    """
    IPrincipal: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-iprincipal

    """

    display_name: str = ComField("DisplayName")
    group_id: str = ComField("GroupId")
    id: str = ComField("Id")
    logon_type: TaskLogonType = EnumField("LogonType", TaskLogonType)
    run_level: TaskRunlevelType = EnumField("RunLevel", TaskRunlevelType)
    user_id: str = ComField("UserId")
    state: "PrincipalState"

    def __init__(self, com_obj):
        super().__init__(com_obj)
        self.state = PrincipalState(self)


class PrincipalState:
    principal: Principle

    def __init__(self, principal: Principle):
        self.principal = principal

    @property
    def run_with_highest_privileges(self) -> bool:
        return self.principal.run_level == TaskRunlevelType.TASK_RUNLEVEL_HIGHEST

    @property
    def run_only_when_user_logged_in(self) -> bool:
        return self.principal.logon_type == TaskLogonType.TASK_LOGON_INTERACTIVE_TOKEN

    @property
    def run_whether_user_is_logged_in_or_not(self) -> bool:
        # run whether user logged in or not:
        # INTERACTIVE_TOKEN_OR_PASSWORD = doesn't store password
        # PASSWORD = stores password
        # S4U = doesn't store password
        return self.principal.logon_type in (
            TaskLogonType.TASK_LOGON_INTERACTIVE_TOKEN_OR_PASSWORD,
            TaskLogonType.TASK_LOGON_PASSWORD,
            TaskLogonType.TASK_LOGON_S4U,
        )

    @property
    def do_not_store_password(self) -> bool:
        # INTERACTIVE_TOKEN_OR_PASSWORD = doesn't store password
        # S4U = doesn't store password
        return self.principal.logon_type in (TaskLogonType.TASK_LOGON_S4U,)

    def set_logon_type(self, must_be_logged_in: bool, store_password: bool):
        """
        Set the login type based on Task Scheduler's user interface.

        We've only covered basic user option here.

        """
        if must_be_logged_in:
            self.principal.logon_type = TaskLogonType.TASK_LOGON_INTERACTIVE_TOKEN

        elif not must_be_logged_in and store_password:
            self.principal.logon_type = TaskLogonType.TASK_LOGON_PASSWORD

        elif not must_be_logged_in and not store_password:
            self.principal.logon_type = TaskLogonType.TASK_LOGON_S4U

        # TODO: there are other possible options we haven't accounted for
        #   and we don't understand how they are applied:
        #     - NONE
        #     - GROUP
        #     - SERVICE_ACCOUNT
