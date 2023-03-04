# -*- coding: utf-8 -*-
import typer
from iscc_eval import speed

cli = typer.Typer(no_args_is_help=True)
cli.add_typer(speed.app, name="speed")

if __name__ == "__main__":
    cli()
