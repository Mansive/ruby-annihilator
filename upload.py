import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import TypedDict


class Config(TypedDict):
    email: str
    password: str
    mega_remote_path: str


def get_config() -> Config:
    DEFAULT_CONFIG = Path(__file__).parent.joinpath("default_config.json")
    USER_CONFIG = Path(__file__).parent.joinpath("config.json")

    with open(DEFAULT_CONFIG) as f:
        config = json.load(f)

    # override default config with user config
    if USER_CONFIG.is_file():
        print("-config.json keys will override counterparts in default_config.json")

        with open(USER_CONFIG) as f:
            user_config = json.load(f)

        for k,v in user_config.items():
            config[k] = v

    return config


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("input_dir", type=dir_path)

    return parser.parse_args()


def dir_path(path):
    if (path := Path(path)).is_dir():
        return path
    else:
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid directory path")
    

def run_cmd(cmd):
    output: str = subprocess.run(cmd if sys.platform == "win32" else shlex.split(cmd), 
                   shell=True, text=True, capture_output=True, encoding="utf8").stdout
    
    print(output, end="")

    return output


def main():
    config = get_config()
    args = get_args()

    remote_path = Path(config['mega_remote_path']).as_posix()
    series_src = Path(args.input_dir)
    
    print(f"-Source: {series_src}\n")
    print("-Logging into Mega...")

    run_cmd(f"mega-login {config['email']} {config['password']}")

    uploads = {}
    series = sorted([entry for entry in series_src.iterdir()
                     if entry.name != "desktop.ini"])
    
    print("-Beginning uploads...")

    for entry in series:
        # Will fail if you replace \" with '
        run_cmd(f"mega-put \"{entry}\" \"{remote_path}\"")

        export_info = run_cmd(f"mega-export -a \"{remote_path}/{entry.name}\"")
        link = re.search(r"https:.*", export_info)

        print()

        # "灼眼のシャナ": https://mega.nz/file/akhdfkjashdiu
        if link := re.search(r"https:.*", export_info):
            uploads[entry.stem] = link.group(0)
        else:
            print("\n[Kuru Kuru Kuru Kuru] what the fuck\n")
    
    with open("uploaded_books.txt", "w", encoding="utf8") as file:
        for name, link in uploads.items():
            file.write(f"{name}\n{link}\n\n")


if __name__ == "__main__":
    main()
