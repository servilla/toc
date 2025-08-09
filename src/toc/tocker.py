#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    toc

:Synopsis:

:Author:
    servilla

:Created:
    8/8/25
"""
import logging
from pathlib import Path

import click
import daiquiri

import tock


CWD = Path(".").resolve().as_posix()
LOGFILE = CWD + "/toc.log"
daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.File(LOGFILE),
        "stdout",
    ),
)
logger = daiquiri.getLogger(__name__)

help_nobackup = "Do not backup the original Markdown file."
help_depth = "Set the maximum depth of the table of contents. (default is -1 for all levels)."

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("md", type=click.Path(exists=True))
@click.option("--nobackup", "-nb", is_flag=True, help=help_nobackup)
@click.option("--depth", "-d", type=int, default=-1, help=help_depth)
def main(md: str, nobackup: bool = False, depth: int = -1):
    """
        Generate and insert a table of contents for the specified Markdown file for all
        Markdown headers by: \n
        1. Adding an anchor element for each header and \n
        2. Inserting the resulting table of contents at the point where it finds the \n
           HTML tag "<!-- TOC -->". \n

        \b
        MD: Markdown file for which to generate a table of contents.
    """

    backup = True
    if nobackup: backup = False

    if Path(md).is_file():
        tock.generate(Path(md), depth=depth, backup=backup)
    else:
        msg = f"Error: Invalid value for 'MD': '{md}' is not is not a regular file."
        print(msg)
        exit(1)


if __name__ == "__main__":
    main()