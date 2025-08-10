# Tocxer: Markdown Table of Contents generator

**Tocxer** is a simple tool to generate a **table of contents** (TOC) for a 
Markdown document that contains ATX-style headers.

To use **Tocxer**, install directly from GitHub by cloning
`https://github.com/servilla/tocxer.git`, create and activate a virtual 
environment (Conda, for example), change directories to the cloned `tocxer`
directory, and run `pip install .`. Once installed, confirm that **Tocxer** is
working by running `tocxer --help`. You should see the following output:

```
tocxer --help
Usage: tocxer [OPTIONS] COMMAND [ARGS]...

  Generate and insert a table of contents for the specified Markdown file for
  all Markdown headers by:

  1. Adding an anchor element for each header and

  2. Inserting the resulting table of contents at the point where it finds the

     HTML tag "<!-- TOC -->".
Options:
  -nb, --nobackup  Do not backup the original Markdown file.
  -h, --help       Show this message and exit.

Commands:
  detocx  Remove all table of contents markers from the specified...
  retocx  Regenerate and insert a table of contents for the specified...
  tocx    Generate and insert a table of contents for the specified...
```
To generate and insert a TOC into a Markdown document, run `tocxer tocx
<file.md>`. By default, **Tocxer** will backup the original Markdown file before
modifying it. To avoid this, use the `--nobackup` option. You can specify the
depth of the ATX header level (e.g., `#`, `##`, ... , `######`) to include in
the TOC with the `--depth <n>` option, where `<n>` is an integer between 1
and 6. If you do not specify a depth, **Tocxer** will use the default depth of 6. 
You can also specify the number of lines to skip from the top of the file 
with the `--skip <n>` option, where `<n>` is an integer. If you do not specify 
a skip, **Tocxer** will use the default skip of 1, ignoring what is 
generally the title header. To remove a **Tocxer** generated TOC from a 
Markdown document, run `tocxer detocx <file.md>`.  To regenerate a TOC for a 
Markdown document that has been modified, run `tocxer retocx <file.md>`: 
this is especially useful if you have modified the Markdown document by adding 
or removing headers. To display help for a specific command, run `tocxer <cmd>
--help`. For example, to display help for the `retocx` command, run 
`tocxer retocx --help`.