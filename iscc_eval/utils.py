# -*- coding: utf-8 -*-
import os
from os.path import basename
from pathlib import Path
from typing import Optional, Tuple
import blake3
import iscc_core
import platform
import cpuinfo
import requests
import iscc_samples
import iscc_sdk as idk
from rich import print
from rich.progress import (
    track,
    Progress,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)
from loguru import logger as log


__all__ = [
    "get_files",
    "system_info",
    "download",
    "iter_files",
    "dirhash",
]


def get_files(path=None, mode=None, recursive=False):
    # type: (Optional[Path],  Optional[str], bool) -> Tuple[int, list]
    """Collect relevant filepaths and total size of data for a given path"""
    if path is None:
        files = list(
            f
            for f in iscc_samples.all()
            if f.suffix not in {".mobi", ".sqlite", ".wav", ".ogg", ".ogv"}
        )
    else:
        file_iter = path.rglob("*") if recursive else path.glob("*")
        files = [p for p in file_iter if p.is_file()]

    if mode is not None:
        filtered_files = []
        for fp in files:
            try:
                mtype, file_mode = idk.mediatype_and_mode(fp.as_posix())
            except idk.IsccUnsupportedMediatype:
                log.debug(f"Unsupported mediatype for {fp.name}")
                continue
            if file_mode == mode:
                filtered_files.append(fp)
        files = filtered_files

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


def download(url, save_to, chunk_size=1000000, force=True):
    """Large (streaming) file download with progress output.

    :param str url: download url
    :param str save_to: file path to save file
    :param int chunk_size: chunk size in bytes
    :param bool force: Force redownload even if file exists
    """
    if force is False:
        if os.path.exists(save_to):
            log.info("Skip download for {}".format(url))
            return save_to

    log.info("Downloading %s -> %s" % (url, save_to))
    r = requests.get(url, stream=True)
    s = int(r.headers["Content-Length"])

    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    )

    with open(save_to, "wb") as f:
        with progress:
            tid = progress.add_task("Download", filename=basename(save_to), total=s)
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    progress.update(tid, advance=chunk_size)
    return save_to


def iter_files(root, exts=None, recursive=False):
    """
    Iterate (recursive) over file paths within root filtered by specified extensions.

    :param str root: Root folder to start collecting files
    :param iterable exts: Restrict results to given file extensions
    :param bool recursive: Wether to walk the complete directory tree
    :rtype collections.Iterable[str]: absolute file paths with given extensions
    """

    if exts is not None:
        exts = set((x.lower() for x in exts))

    def matches(e):
        return (exts is None) or (e in exts)

    if recursive is False:
        for entry in os.scandir(root):
            ext = os.path.splitext(entry.name)[-1].lstrip(".").lower()
            if entry.is_file() and matches(ext):
                yield entry.path
    else:
        for root, folders, files in os.walk(root):
            for f in files:
                ext = os.path.splitext(f)[-1].lstrip(".").lower()
                if matches(ext):
                    yield os.path.join(root, f)


def dirhash(path: Path):
    read_size = 2097152
    files = sorted(f for f in path.rglob("*") if f.is_file())
    hasher = blake3.blake3()
    print(f"Calculating directory hash for {len(files)} files in {path}")
    for file in track(files, description="Verifying..."):
        with open(file, "rb") as infile:
            data = infile.read(read_size)
            while data:
                hasher.update(data)
                data = infile.read(read_size)
    return hasher.hexdigest()
