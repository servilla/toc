#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    tock

:Synopsis:

:Author:
    servilla

:Created:
    8/8/25
"""
from dataclasses import dataclass
from pathlib import Path
import re

import daiquiri


logger = daiquiri.getLogger(__name__)


@dataclass
class Header:
    """Represents a markdown header with its properties."""
    level: int
    text: str
    anchor: str
    line_number: int
    original_line: str


def tock(md: Path, depth: int = 6, skip: int = 1, backup: bool = True):
    """
    Generates and inserts a Table of Contents (TOC) into a Markdown file. This function identifies
    ATX-formatted headers in the given Markdown file, creates anchors for navigation, and optionally
    backs up the original file before making modifications. The function injects the TOC at a designated
    placeholder and ensures navigation anchors are added to each header and the top of the file.

    Parameters:
        md (Path): Path object representing the Markdown file to be modified.
        depth (int): The maximum depth of headers to include in the Table of Contents. Defaults to 6
                     (all depths).
        skip (int): Number of initial lines to skip when parsing the file for headers or placeholder.
                    Defaults to 1.
        backup (bool): Whether to create a backup of the file before making modifications. Defaults to True.

    Raises:
        OSError: If file operations such as reading or writing fail.
        ReError: If regular expression matching fails during processing.

    Returns:
        None
    """
    headers = []

    with md.open() as f:
        lines = f.readlines()

    if backup:
        md.rename(md.with_suffix(".md.bak"))

    toc_insert_line = None
    for line_no in range(skip, len(lines)):
        line = lines[line_no]

        if re.match(r"<!-- TOC -->", line):
            toc_insert_line = line_no

        # Build ATX header index
        atx_match = re.match(r"^(#{1,6})\s+(.+)", line)
        if atx_match:
            level = len(atx_match.group(1))
            if level <= depth:
                text = atx_match.group(2)
                anchor = _create_anchor(text)
                header = Header(level, text, anchor, line_no, line)
                headers.append(header)
                lines[line_no] = f"{line.rstrip()} <a id=\"{anchor}\"></a> [^](#top)\n"

    # Add top anchor to first line
    lines[0] = f"{lines[0].rstrip()} <a id=\"top\"></a>\n"

    toc = _build_toc(headers)
    if toc_insert_line is not None:
        lines.insert(toc_insert_line, "".join(toc))

    with md.open("w") as f:
        f.writelines(lines)

def _create_anchor(text: str) -> str:
    """
    Create an anchor link from header text.

    This follows common markdown anchor conventions:
    - Convert to lowercase
    - Replace spaces and special chars with hyphens
    - Remove multiple consecutive hyphens
    """
    # Remove HTML tags if present
    text = re.sub(r'<[^>]+>', '', text)

    # Convert to lowercase and replace spaces/special chars with hyphens
    anchor = re.sub(r'[^\w\s-]', '', text).strip()
    anchor = re.sub(r'[-\s]+', '-', anchor).lower()

    # Remove leading/trailing hyphens
    anchor = anchor.strip('-')

    return anchor


def _build_toc(headers: list) -> list:
    """Build a table of contents from a list of headers."""
    tab = "    "
    min_toc_depth = _min_toc_depth(headers)  # For list indention
    toc = ["## Table of Contents\n"]
    for header in headers:
        toc_header = f"{tab * (header.level - min_toc_depth)}* [{header.text}](#{header.anchor})\n"
        toc.append(toc_header)

    return toc


def _min_toc_depth(headers: list) -> int:
    """Determine the minimum depth of the TOC."""
    min_toc_depth = 6  # Max depth of Markdown headers
    for header in headers:
        if header.level < min_toc_depth:
            min_toc_depth = header.level
    return min_toc_depth

def detock(md: Path, backup: bool = True):

    with md.open() as f:
        lines = f.readlines()

    if backup:
        md.rename(md.with_suffix(".md.bak"))

    # Remove TOC
    toc_begin_line = _get_toc_begin(lines)
    toc_end_line = _get_toc_end(lines)
    if toc_begin_line is not None and toc_end_line is not None:
        del lines[toc_begin_line:toc_end_line]

    # Remove all anchors
    top = re.escape("[^](#top)")
    for line_no in range(len(lines)):
        line = lines[line_no]
        lines[line_no] = re.sub(fr"\s<a id=\".*\"></a> {top}", "", line)

    with md.open("w") as f:
        f.writelines(lines)


def _get_toc_begin(lines: list) -> int:
    """Determine the line number of the TOC begin headerr."""
    toc_begin_line = None
    for line_no in range(len(lines)):
        line = lines[line_no]
        if re.match(r"## Table of Contents", line):
            toc_begin_line = line_no
            break
    return toc_begin_line


def _get_toc_end(lines: list) -> int:
    """Determine the line number of the TOC marker."""
    toc_end_line = None
    for line_no in range(len(lines)):
        line = lines[line_no]
        if re.match(r"<!-- TOC -->", line):
            toc_end_line = line_no
            break
    return toc_end_line


def retock(md: Path, depth: int = 6, skip: int = 1, backup: bool = True):
    detock(md, backup=backup)
    tock(md, depth=depth, skip=skip, backup=backup)
