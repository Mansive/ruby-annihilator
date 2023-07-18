import argparse
import subprocess
import sys
import shlex
from pathlib import Path


ARCHIVE_TYPE = "-t7z"
REGEX = "-xr0!*desktop.ini"


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("input_dir", type=dir_path)
    parser.add_argument("output_dir", type=dir_path)

    return parser.parse_args()


def dir_path(path):
    path = Path(path)
    if path.is_dir():
        return path
    else:
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid directory path")


def run_cmd(cmd):
    subprocess.run(cmd if sys.platform == "win32" else shlex.split(cmd))


def main():
    args = get_args()

    series_src = Path(args.input_dir)
    dest = Path(args.output_dir)

    print(f"Source: {series_src}")
    print(f"Destination: {dest}")

    series = [entry for entry in series_src.iterdir() if entry.name != "desktop.ini"]

    for entry in series:
        if (series_src := entry).is_dir():
            series_src /= "*"

        series_zip = dest / (entry.stem + ".7z")

        run_cmd(f"7z a {ARCHIVE_TYPE} {REGEX} \"{series_zip}\" \"{series_src}\"")


if __name__ == "__main__":
    main()
