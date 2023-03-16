# -*- coding: utf-8 -*-
import typer
from iscc_eval import state, config, speed, match
from rich import print


cli = typer.Typer(no_args_is_help=True)


@cli.callback()
def main(verbose: bool = False):
    """
    Manage users in the awesome CLI app.
    """
    if verbose:
        print("Will produce verbose output")
        state["verbose"] = True


cli.add_typer(speed.app, name="speed")
cli.add_typer(config.app, name="config")
cli.add_typer(match.app, name="match")


if __name__ == "__main__":
    cli()
