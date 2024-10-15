from tasksch import TaskService
from ..utils import console
from .shared import create_demo_folder
from .shared import DEMO_FOLDER_NAME


def main(ts: TaskService):
    console.print("[yellow]DEMO[/yellow] Creat Folder")
    if create_demo_folder(ts):
        console.print(f"     The demo folder \\{DEMO_FOLDER_NAME} created!")
        return
    console.print(f"     The demo folder \\{DEMO_FOLDER_NAME} already exists!")
