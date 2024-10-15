from .cli import create_cli_parser
from .utils import console


def run():
    cli_parser = create_cli_parser()
    cli_args = cli_parser.parse_args()
    try:
        cli_args.func(cli_args)
    except Exception as ex:
        # TODO: make this a little more visible
        err_msg = str(ex)
        console.print("-" * 60)
        console.print(err_msg)
        console.print("-" * 60)
        import traceback

        console.print(traceback.format_exc())
        console.print("-" * 60)
