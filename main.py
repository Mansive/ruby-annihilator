"""Fixes Yomichan sentence extraction on epubs by removing <rb> tags"""

import argparse
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("input_dir", type=str)
    parser.add_argument("output_dir", type=str)

    return parser.parse_args()


def validate_dir(path: Path) -> None:
    if not path.is_dir():
        raise RuntimeError(f"Invalid directory: {path}")


def main():
    args = get_args()

    src = Path(args.input_dir)
    validate_dir(src)
    print(f"Source: {src}")

    dest = Path(args.output_dir)
    validate_dir(dest)
    print(f"Destination: {dest}")

    print("\n-Running; let it cook...")

    epubs = [entry for entry in src.rglob("*") if entry.suffix == ".epub"]
    epubs_total = len(epubs)
    count = 0

    for epub in epubs:
        count += 1
        print(f"-PROCESSING {count}/{epubs_total}: {epub.name}")
        

        # Recreate directory tree of epub relative to its current working directory
        new_epub = dest.joinpath(epub.relative_to(src))
        new_epub.parent.mkdir(parents=True, exist_ok=True)

        # DEFLATE used for compatibility with ttu and Calibre
        with ZipFile(epub, "r") as zip, ZipFile(new_epub, "w", ZIP_DEFLATED) as new_zip:
            for file_path in zip.namelist():
                with zip.open(file_path, "r") as file:
                    text = file.read()

                    if "html" in file_path[-4:]:
                        text = re.sub(b"</?rb>", b"", text)

                    new_zip.writestr(file_path, text) 
    
    print(f"-Finished processing {count} books")

if __name__ == "__main__":
    main()
