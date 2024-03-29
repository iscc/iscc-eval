from pathlib import Path
from typing import Optional, List, Callable
import iscc_sdk as idk
import typer
from codetiming import Timer
from humanize import naturalsize as nsize
import iscc_eval as ie
from rich.console import Console


out = Console()
app = typer.Typer(no_args_is_help=True, help="ISCC execution speed benchmarks")


@app.command()
def instance_code(path: Optional[Path] = typer.Argument(None)):
    """Benchmark Instance-Code processing speed."""
    total, files = ie.get_files(path, recursive=True)
    out.print(ie.system_info("Instance-Code"))
    out.print(f"Benchmarking with {len(files)} files (total size: {nsize(total)}) on single core.")
    result = speed_benchmark(files, idk.code_instance, total)
    out.print(result)


@app.command()
def data_code(path: Optional[Path] = typer.Argument(None)):
    """Benchmark Data-Code processing speed."""
    total, files = ie.get_files(path, recursive=True)
    out.print(ie.system_info("Data-Code"))
    out.print(f"Benchmarking with {len(files)} files (total size: {nsize(total)}) on single core.")
    result = speed_benchmark(files, idk.code_data, total)
    out.print(result)


@app.command()
def content_code(path: Optional[Path] = typer.Argument(None)):
    """Benchmark Content-Code processing speed."""
    total, files = ie.get_files(path, recursive=True)
    out.print(ie.system_info("Content-Code"))
    out.print(f"Benchmarking with {len(files)} files (total size: {nsize(total)}) on single core.")
    result = speed_benchmark(files, idk.code_content, total)
    out.print(result)


@app.command()
def meta_code(path: Optional[Path] = typer.Argument(None)):
    """Benchmark Meta-Code processing speed."""
    total, files = ie.get_files(path, recursive=True)
    out.print(ie.system_info("Content-Code"))
    out.print(f"Benchmarking with {len(files)} files (total size: {nsize(total)}) on single core.")
    result = speed_benchmark(files, idk.code_meta, total)
    out.print(result)


@app.command()
def iscc_code(path: Optional[Path] = typer.Argument(None)):
    """Benchmark ISCC-CODE processing speed."""
    total, files = ie.get_files(path, recursive=True)
    out.print(ie.system_info("ISCC-CODE"))
    out.print(f"Benchmarking with {len(files)} files (total size: {nsize(total)}) on single core.")
    result = speed_benchmark(files, idk.code_iscc, total)
    out.print(result)


def speed_benchmark(files: List[Path], func: Callable, total: Optional[int]):
    nbytes = total or sum(file.stat().st_size for file in files)
    nfiles = len(files)
    with Timer(logger=None) as t:
        for file in files:
            r = func(str(file))
            out.print(f"Processed {file.name} -> {r.iscc}")
    bytes_per_second = nbytes / t.last
    return f"\n[bold yellow on red]Result: {nsize(bytes_per_second)}/second (with {nfiles} files)\n"


if __name__ == "__main__":
    app()
