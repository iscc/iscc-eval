# -*- coding: utf-8 -*-
from pathlib import Path
import typer
from iscc_eval import state, config, speed, match
from rich import print as rprint
import iscc_sdk as idk
import iscc_core as ic


cli = typer.Typer(no_args_is_help=True)


@cli.callback()
def main(verbose: bool = False):
    if verbose:
        rprint("Will produce verbose output")
        state["verbose"] = True


@cli.command()
def cc(
    path: Path = typer.Argument(..., help="Path to file for Content-Code processing"),
    bits: int = typer.Option(64, help="Content-Code length in number of bits (64, 128, 256)"),
):
    """Generate Content-Code for File"""
    idk.sdk_opts.extract_metadata = False
    ic.core_opts.audio_bits = bits
    ic.core_opts.image_bits = bits
    ic.core_opts.text_bits = bits
    ic.core_opts.video_bits = bits
    assert bits in (64, 128, 256)
    iscc_meta = idk.code_content(path.as_posix())
    print(iscc_meta.iscc)


@cli.command()
def distance(a: str, b: str):
    """Calculate distance between ISCC-CODES A and B"""
    dist = ic.iscc_distance(a, b)
    print(dist)


cli.add_typer(speed.app, name="speed")
cli.add_typer(config.app, name="config")
cli.add_typer(match.app, name="match")


if __name__ == "__main__":
    cli()
