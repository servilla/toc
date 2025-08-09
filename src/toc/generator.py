#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    generator

:Synopsis:

:Author:
    servilla

:Created:
    8/8/25
"""
from pathlib import Path
import re

import daiquiri


logger = daiquiri.getLogger(__name__)


def generate(md: Path, depth: int = -1, backup: bool = True):


    with md.open() as f:
        lines = f.readlines()

    if backup:
        md.rename(md.with_suffix(".md.bak"))

    toc_insert_str = "<!-- TOC -->"
    toc_insert_line = 0
    for line_no in range(len(lines)):
        if toc_insert_str in lines[line_no]:
            toc_insert_line = line_no
            break

    hashes = "#"
    if depth == -1:
        pattern = fr"^#+ "
    else:
        hashes = "#" * depth
        pattern = fr"^{hashes}?(?!#) "

    toc = ["## Table of Contents\n"]
    min_toc_depth = len(hashes)
    for line_no in range(toc_insert_line + 1, len(lines)):
        line = lines[line_no]
        if re.match(pattern, line):
            header_level = line.split(" ", maxsplit=1)[0]
            header = line.split(" ", maxsplit=1)[1]
            anchor_header = (re.sub(r'[^a-zA-Z]+', ' ', header)).strip().lower().replace(" ", "_")
            anchor = f"<a id=\"{anchor_header}\"></a>"
            lines[line_no] = f"{header_level} {anchor} {header.strip()} [^](#top)\n"
            if len(header_level) < min_toc_depth:
                min_toc_depth = len(header_level)
            toc_depth = len(header_level)
            toc.append(f"{'    ' * toc_depth}* [{header.strip()}](#{anchor_header})\n")

    for i in range(1, len(toc)):
        toc[i] = toc[i][min_toc_depth * 4:]

    lines.insert(0, "<a id=\"top\"></a>\n")
    lines[toc_insert_line:toc_insert_line + 1] = toc

    with md.open("w") as f:
        f.writelines(lines)

