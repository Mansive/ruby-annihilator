import argparse
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


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


def main():
    args = get_args()

    src = Path(args.input_dir)
    dest = Path(args.output_dir)

    print(f"Source: {src}")
    print(f"Destination: {dest}\n")

    epubs = [entry for entry in src.rglob("*") if entry.suffix == ".epub"]
    epubs_total = len(epubs)
    count = 0

    for epub in epubs:
        count += 1
        print(f"-PROCESSING {count}/{epubs_total}: {epub.name}")
        
        # Recreate directory tree of epub relative to source folder
        new_epub = dest.joinpath(epub.relative_to(src))
        new_epub.parent.mkdir(parents=True, exist_ok=True)

        # DEFLATE used for compatibility with ttu Reader and Calibre
        with ZipFile(epub, "r") as zip, ZipFile(new_epub, "w", ZIP_DEFLATED) as new_zip:
            for file_path in zip.namelist():
                with zip.open(file_path, "r") as file:
                    text: bytes = file.read()

                    if "html" in file_path[-4:]:
                        text = re.sub(b"</?rb>", b"", text)

                    new_zip.writestr(file_path, text) 
    
    print(f"-Finished processing {count} books\n")

if __name__ == "__main__":
    main()
