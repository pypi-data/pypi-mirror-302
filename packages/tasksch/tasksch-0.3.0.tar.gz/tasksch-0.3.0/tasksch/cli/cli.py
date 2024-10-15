import argparse
from .display_cmd import display_command
from .list_cmd import list_command
from .demos import demo_command


def create_cli_parser() -> argparse.ArgumentParser:
    program = argparse.ArgumentParser(prog="tasksch")
    program.set_defaults(func=lambda x: program.print_help())
    commands = program.add_subparsers()

    list_cmd = commands.add_parser("list", help="Show list of folder and task names.")
    list_cmd.set_defaults(func=list_command)

    folder_group = list_cmd.add_mutually_exclusive_group()
    folder_group.add_argument("--folders", action="store_true", help="Include folders in list.")
    folder_group.add_argument("--folder-filter", help="Apply regular rexpression to filter folder names.")

    task_group = list_cmd.add_mutually_exclusive_group()
    task_group.add_argument("--tasks", action="store_true", help="Include tasks in list.")
    task_group.add_argument("--task-filter", help="Apply regular expression to filter task names.")

    display_cmd = commands.add_parser("display", help="Show task details.")
    display_cmd.set_defaults(func=display_command)
    display_cmd.add_argument("--folder-filter", help="Apply regular expression to filter folders by name.")
    display_cmd.add_argument("--task-filter", help="Apply regular expression to filter tasks by name.")
    display_cmd.add_argument("--show-general", action="store_true", help="Display task general task definitions.")
    display_cmd.add_argument("--show-settings", action="store_true", help="Display task settings definitions.")
    display_cmd.add_argument("--show-triggers", action="store_true", help="Display task trigger definitions.")
    display_cmd.add_argument("--show-actions", action="store_true", help="Display task action definitions.")

    demo_cmd = commands.add_parser("demo", help="Create basic tasks for demonstration purposes.")
    demo_cmd.set_defaults(func=demo_command)
    demo_cmd.add_argument("--time-trigger", action="store_true", help="Create a demo task with a time trigger.")
    demo_cmd.add_argument("--daily-trigger", action="store_true", help="Create a demo task with a daily trigger.")
    demo_cmd.add_argument("--weekly-trigger", action="store_true", help="Create a demo task with weekly trigger.")
    demo_cmd.add_argument("--monthly-trigger", action="store_true", help="Create a demo task with a monthly trigger.")
    demo_cmd.add_argument("--monthlydow-trigger", action="store_true", help="Create a demo task with a Monthly DOW trigger.")
    demo_cmd.add_argument("--delete-all", action="store_true", help="Delete all demo tasks.")
    demo_cmd.add_argument("--refresh", action="store_true", help="If the task already exists, first delete and then re-create.")
    demo_cmd.add_argument("--suffix", help="Apply a suffix to the task name.")
    demo_cmd.add_argument("--set-logged-in-only", action="store_true", help="Task only operates when owner logged in.")
    demo_cmd.add_argument("--set-store-password", action="store_true", help="Store the owner's password.")

    return program
