# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Optional
import iscc_core
import platform
import cpuinfo
import iscc_samples

__all__ = [
    "get_files",
    "system_info",
]


def get_files(path: Optional[Path] = None):
    if path is None:
        files = list(iscc_samples.all())
    else:
        files = [p for p in path.rglob("*") if p.is_file()]
    total = sum(f.stat().st_size for f in files)
    return total, files


def system_info(name=""):
    """Printable system info"""
    cinfo = cpuinfo.get_cpu_info()
    sinfo = (
        "\n[bold]ISCC Performance Benchmark - {}[/bold]\n"
        "==========================================================================\n"
        "CPU:     {}\n"
        "Cores:   {}\n"
        "OS:      {}\n"
        "Python:  {} - {} - {}\n"
        "ISCC:    {}\n"
        "==========================================================================\n"
    ).format(
        name,
        cinfo.get("brand_raw"),
        cinfo.get("count"),
        platform.platform(),
        platform.python_implementation(),
        platform.python_version(),
        platform.python_compiler(),
        iscc_core.__version__,
    )
    return sinfo
