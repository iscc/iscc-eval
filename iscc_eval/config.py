# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import Optional
from rich import print
import typer
from pydantic import BaseSettings, Field, DirectoryPath
import iscc_eval as ie
from loguru import logger as log


__all__ = ["cnf"]

app = typer.Typer(no_args_is_help=True, help="ISCC evaluation framework configuration")


class IsccEvalSettings(BaseSettings):
    """Evaluation framework configuration"""

    class Config:
        validate_assignment = True

    data_dir: DirectoryPath = Field(
        ie.DEFAULT_DATA_DIR, description="Root directory for evaluation data"
    )

    def save(self):
        """Save settings"""
        with open(ie.SETTINGS_PATH, "wt", encoding="utf8") as outf:
            outf.write(self.json())

    @staticmethod
    def load():
        global cnf
        if ie.SETTINGS_PATH.exists():
            with open(ie.SETTINGS_PATH, "rt", encoding="utf8") as infile:
                data = json.loads(infile.read())
            cnf = IsccEvalSettings(**data)
        else:
            cnf = IsccEvalSettings()


cnf: Optional[IsccEvalSettings] = None


try:
    IsccEvalSettings.load()
except Exception as e:
    log.error(f"Failed to load settings from {ie.SETTINGS_PATH}. Using default settings")
    cnf = IsccEvalSettings()


@app.command()
def show():
    """Show current configuration"""
    for k, v in cnf.dict().items():
        print(f"{k} = {v}")


@app.command(name="set")
def set_(key: str, value: str):
    """Set a specific configuration value"""
    if key == "data_dir":
        path = Path(value)
        if not path.exists():
            log.debug(f"Creating data_dir at {path}")
            path.mkdir(parents=True)
    setattr(cnf, key, value)
    cnf.save()
    print("\nNew Settings:\n")
    for k, v in cnf.dict().items():
        print(f"{k} = {v}")


@app.command()
def reset():
    """Reset configuration to default settings"""
    print(f"Deleting {ie.SETTINGS_PATH}")
    ie.SETTINGS_PATH.unlink(missing_ok=True)
