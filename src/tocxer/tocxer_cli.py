#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    tocker_cli

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

from tocxer import tocxs


CWD = Path(".").resolve().as_posix()
LOGFILE = CWD + "/tocxer.log"
daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.File(LOGFILE),
        "stdout",
    ),
)
logger = daiquiri.getLogger(__name__)

help_nobackup = "Do not backup the original Markdown file."
help_depth = "Set the maximum depth of the table of contents. (default is 6 for all levels)."
help_skip = "Skip the first N lines."

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("--nobackup", "-nb", is_flag=True, help=help_nobackup)
@click.pass_context
def tocxer(ctx, nobackup: bool = False):
    """
        Generate and insert a table of contents for the specified Markdown file for all
        Markdown headers by: \n
        1. Adding an anchor element for each header and \n
        2. Inserting the resulting table of contents at the point where it finds the \n
           HTML tag "<!-- TOC -->". \n
    """
    ctx.obj = {"nobackup": nobackup}


@tocxer.command(context_settings=CONTEXT_SETTINGS)
@click.argument("md", type=str)
@click.option("--depth", "-d", type=int, default=6, help=help_depth)
@click.option("--skip", "-s", type=int, default=1, help=help_skip)
@click.pass_context
def tocx(ctx, md: str, depth: int = 6, skip: int = 1):
    """
        Generate and insert a table of contents for the specified Markdown file. \n

        \b
        MD: Markdown file for which to insert a table of contents.
    """

    backup = True
    if ctx.obj["nobackup"]: backup = False

    if Path(md).exists and Path(md).is_file():
        tocxs.tocx(Path(md), depth=depth, skip=skip, backup=backup)
    else:
        msg = f"Error: Invalid value for 'MD': '{md}' does not exist or is not a regular file."
        print(msg)
        exit(1)


@tocxer.command(context_settings=CONTEXT_SETTINGS)
@click.argument("md", type=str)
@click.pass_context
def detocx(ctx, md: str):
    """
        Remove all table of contents markers from the specified Markdown file. \n

        \b
        MD: Markdown file for which to remove a table of contents.
    """

    backup = True
    if ctx.obj["nobackup"]: backup = False

    if Path(md).exists and Path(md).is_file():
        tocxs.detocx(Path(md), backup=backup)
    else:
        msg = f"Error: Invalid value for 'MD': '{md}' does not exist or is not a regular file."
        print(msg)
        exit(1)


@tocxer.command(context_settings=CONTEXT_SETTINGS)
@click.argument("md", type=str)
@click.option("--depth", "-d", type=int, default=6, help=help_depth)
@click.option("--skip", "-s", type=int, default=1, help=help_skip)
@click.pass_context
def retocx(ctx, md: str, depth: int = 6, skip: int = 1):
    """
        Regenerate and insert a table of contents for the specified Markdown file. \n

        \b
        MD: Markdown file for which to reinsert a table of contents.
    """

    backup = True
    if ctx.obj["nobackup"]: backup = False

    if Path(md).exists and Path(md).is_file():
        tocxs.retocx(Path(md), depth=depth, skip=skip, backup=backup)
    else:
        msg = f"Error: Invalid value for 'MD': '{md}' does not exist or is not a regular file."
        print(msg)
        exit(1)


if __name__ == "__main__":
    tocxer(obj={})