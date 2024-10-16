import argparse
import pathlib
import sys

from logoizer._version import __version__
from logoizer.api import logoize as logoize_


def _logoize(words, yes, output, format, theme):
    if output is None:
        output = sys.stdout
    elif pathlib.Path(output).exists() and not yes:
        confirm = input("file exists, overwrite? [y/N]: ")
        if confirm.lower() != "y":
            print("Aborted.")
            sys.exit(1)
    logoize_(words.strip(), output, format=format, light=(theme == "light"))


def main():
    parser = argparse.ArgumentParser(
        description="Logoize words into a specified format and theme."
    )
    parser.add_argument(
        "--version", action="version", version=f"logoizer {__version__}"
    )
    parser.add_argument("words", type=str, help="Words to convert into a logo")
    parser.add_argument(
        "--yes", action="store_true", help="Do not prompt for confirmation"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=("png", "svg"),
        default=None,
        help="Format of the output file",
    )
    parser.add_argument(
        "--theme",
        "-t",
        choices=("light", "dark"),
        default="light",
        help="Theme for the logo (default: light)",
    )

    args = parser.parse_args()

    if args.output is not None and pathlib.Path(args.output).exists() and not args.yes:
        confirm = input("file exists, overwrite? [y/N]: ")
        if confirm.lower() != "y":
            print("Aborted.")
            sys.exit(1)

    logoize_(
        args.words.strip(),
        sys.stdout if args.output is None else args.output,
        format=args.format,
        light=(args.theme == "light"),
    )


if __name__ == "__main__":
    main()
