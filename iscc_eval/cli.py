# -*- coding: utf-8 -*-
from codetiming import Timer
from typing import Callable, List, Optional
import typer
from pathlib import Path
import iscc
from iscc_eval.utils import system_info
import iscc_samples
from humanize import naturalsize as nsize

cli = typer.Typer(
    add_completion=False,
)


@cli.command()
def instance_code(path: Optional[Path] = typer.Argument(None)):
    """Benchmark Instance-Code processing speed."""
    total, files = get_files(path)
    typer.echo(system_info("Instance-Code"))
    typer.echo(f"Benchmarking with {len(files)} files (total size: {nsize(total)}).")
    result = speed_benchmark(files, iscc.code_instance, total)
    typer.echo(result)


@cli.command()
def data_code(path: Optional[Path] = typer.Argument(None)):
    """Benchmark Data-Code processing speed."""
    total, files = get_files(path)
    typer.echo(system_info("Instance-Code"))
    typer.echo(f"Benchmarking with {len(files)} files (total size: {nsize(total)}).")
    result = speed_benchmark(files, iscc.code_data, total)
    typer.echo(result)


def get_files(path: Optional[Path] = None):
    if path is None:
        files = list(iscc_samples.all())
    else:
        files = [p for p in path.rglob("*") if p.is_file()]
    total = sum(f.stat().st_size for f in files)
    return total, files


def speed_benchmark(files: List[Path], func: Callable, total: Optional[int]):
    nbytes = total or sum(file.stat().st_size for file in files)
    nfiles = len(files)
    with Timer(logger=None) as t:
        for file in files:
            func(file)
    bytes_per_second = nbytes / t.last
    return f"Result: {nsize(bytes_per_second)}/second (with {nfiles} files)"


if __name__ == "__main__":
    cli()
