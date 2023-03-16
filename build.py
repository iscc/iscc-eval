# -*- coding: utf-8 -*-
import PyInstaller.__main__
import platform

# fmt: off
cmd = [
        "iscc_eval/cli.py",
        "--clean",
        "--console",
        "--name", "iscc-eval",
]
# fmt: on

if platform.system() != "Darwin":
    cmd.append("--onefile")

PyInstaller.__main__.run(cmd)
