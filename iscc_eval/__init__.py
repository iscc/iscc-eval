import os
import sys
from pathlib import Path
import click
from loguru import logger
from rich.console import Console

logger.remove()
logger.add(sys.stderr, level="CRITICAL")

ROOT_DIR = Path(__file__).parent.parent.resolve().absolute()
DATA_DIR = ROOT_DIR / "data"


APP_NAME = "iscc-eval"
APP_DIR = Path(click.get_app_dir(APP_NAME, roaming=False))
DEFAULT_DATA_DIR = Path(APP_DIR) / "data"
SETTINGS_PATH = APP_DIR / "settings.json"
state = {"verbose": False}
out = Console()

if not os.path.exists(APP_DIR):
    os.makedirs(DEFAULT_DATA_DIR)

from iscc_eval.config import *
from iscc_eval.utils import *
from iscc_eval.datasets.fma_small import *
