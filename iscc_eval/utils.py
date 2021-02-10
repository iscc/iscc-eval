# -*- coding: utf-8 -*-
import iscc
import platform
import cpuinfo


def system_info(name=""):
    """Printable system info"""
    cinfo = cpuinfo.get_cpu_info()
    sinfo = (
        "ISCC Performance Benchmark - {}\n"
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
        iscc.__version__,
    )
    return sinfo


if __name__ == "__main__":
    print(system_info())
