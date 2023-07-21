import argparse
import subprocess
import sys
import shlex
from pathlib import Path
from zipfile import ZIP_LZMA, ZipFile


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

    src = Path(args.input_dir)
    dest = Path(args.output_dir)

    print(f"-Source: {src}")
    print(f"-Destination: {dest}\n")

    series = [entry for entry in src.iterdir() if entry.name != "desktop.ini"]
    series_total = len(series)
    count = 0

    for entry in series:
        count += 1
        print(f"-Extracting {count}/{series_total}: {entry.name}")

        manga_path = dest / entry.stem

        with ZipFile(entry, "r") as epub:
            for path in epub.infolist():
                if "OEBPS/image/" in path.filename:
                   # Extract to "/" instead of "OEBPS/image/"
                   path.filename = Path(path.filename).name
                   epub.extract(path, manga_path)

    print(f"\n-Finished extracting {count} series\n")


if __name__ == "__main__":
    main()
