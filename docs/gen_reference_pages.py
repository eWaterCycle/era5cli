import mkdocs_gen_files
from era5cli import inputref
import era5cli.cli
import subprocess
from typing import List, Generator


def divide_chunks(biglist: List, n: int) -> Generator[List, None, None]:
    """Divide a list in n-sized chunks"""
    for i in range(0, len(biglist), n):
        yield biglist[i : i + n]


def add_padding(multiline_string: List[str]):
    """Add a 4-spaces padding to the start of every line."""
    multiline_string = multiline_string.replace("\n", "\n    ")
    return f"    {multiline_string}"


# Build the variable reference markdown file from the input reference.
filename = "reference/variables.md"

variable_data = [  # Full name, short name, inputreference, number of columns:
    ("Available single level variables", "2D vars", inputref.PLVARS, 3),
    ("Available pressure level variables", "3D vars", inputref.SLVARS, 2),
    (
        "Available pressure levels",
        "Pressure levels",
        [str(p) for p in inputref.PLEVELS],
        4,
    ),
    ("Available ERA5-land variables", "ERA5-Land", inputref.ERA5_LAND_VARS, 2),
]


filename = "reference/variables.md"  # Already exists, has the introductory text


with mkdocs_gen_files.open(filename, "a") as f:  # Only append to file (!)
    for full_name, short_name, ref, ncol in iter(variable_data):
        print("", file=f)
        print(f'=== "{short_name}"', file=f)
        print("", file=f)
        print(f"    | {full_name} |{' |' * (ncol - 1)}", file=f)
        print(f"    |{'-|' * ncol}", file=f)
        for chunk in divide_chunks(ref, ncol):
            print(f"    |{'|'.join(chunk)}|", file=f)
        print("", file=f)


# Build the CLU usage reference docs:
filename = "reference/cli_usage.md"  # Already exists, has the introductory text


with mkdocs_gen_files.open(filename, "a") as f:  # Only append to file (!)
    parser = era5cli.cli._build_parser()
    parser_help = parser.format_help()
    parser_help = parser_help.replace("`", "'")
    parser_help = "\n".join(parser_help.split("\n")[2:])
    print("```", file=f)
    print("$ era5cli --help", file=f)
    print("", file=f)
    print(parser_help, file=f)
    print("```", file=f)


# Build the argument reference docs:
filename = "reference/arguments.md"  # Already exists, has the introductory text

with mkdocs_gen_files.open(filename, "a") as f:  # Only append to file (!)
    subparsers = ["Hourly", "Monthly"]

    for subp in subparsers:
        with subprocess.Popen(
            ["era5cli", subp.lower(), "--help"], stdout=subprocess.PIPE
        ) as process:
            stdout, stderr = process.communicate()
        helpstr = stdout.decode("utf-8")
        helpstr = helpstr[helpstr.index("optional arguments") :]

        # Split out \r\n (for Windows only?)
        split_str = helpstr.splitlines()
        helpstr = "\n".join(split_str)

        print("", file=f)
        print(f'=== "{subp}"', file=f)
        print("", file=f)
        print("    ```", file=f)
        print(f"    $ era5cli {subp.lower()} --help", file=f)
        print("    ", file=f)
        print(add_padding(helpstr), file=f, end=None)
        print("    ```", file=f)

mkdocs_gen_files.set_edit_path(filename, "gen_reference_pages.py")
