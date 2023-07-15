"""Fixes Yomichan sentence extraction on epubs by removing <rb> tags"""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("input_dir", type=str)
    parser.add_argument("output_dir", type=str)

    return parser.parse_args()


def remove_rb(text: str) -> str:
    return text.replace("<rb>", "").replace("</rb>", "")


def validate_dir(path: Path) -> None:
    if not path.is_dir():
        raise RuntimeError(f"Invalid directory: {path}")


def main():
    args = get_args()

    src = Path(args.input_dir)
    validate_dir(src)

    dest = Path(args.output_dir)
    validate_dir(dest)

    print("-Running; let it cook...")

    epubs = [entry for entry in src.rglob("*") if entry.suffix == ".epub"]
    count = 0

    for epub in epubs:
        print(f"-PROCESSING: {epub.name}")
        count += 1

        # Recreate directory tree of epub relative to its current working directory
        new_epub = dest.joinpath(epub.relative_to(src))
        new_epub.parent.mkdir(parents=True, exist_ok=True)

        with ZipFile(epub, "r") as zip, ZipFile(new_epub, "w", ZIP_DEFLATED) as new_zip:
            for file_path in zip.namelist():
                with zip.open(file_path, "r") as file:
                    text: str | bytes

                    if ".xhtml" in file_path:
                        text = remove_rb(file.read().decode("utf-8"))
                    else:
                        text = file.read()

                    new_zip.writestr(file_path, text) 
    
    print(f"-Finished processing {count} books")

if __name__ == "__main__":
    main()
