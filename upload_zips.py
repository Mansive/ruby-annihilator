"""Doesn't work on Python 3.11 cause reasons"""
import argparse
import json
from mega import Mega
from pathlib import Path
from typing import TypedDict


class Config(TypedDict):
    email: str
    password: str


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
    path = Path(path)
    if path.is_dir():
        return path
    else:
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid directory path")


def main():
    config = get_config()
    args = get_args()

    series_src = Path(args.input_dir)

    print(f"Source: {series_src}\n")
    print("-Logging into Mega...")

    mega = Mega()
    m = mega.login(config["email"], config["password"])

    print("-Login successful! Starting upload process...")

    series = [entry for entry in series_src.iterdir() if entry.name != "desktop.ini"]

    for entry in series:
        file = m.upload(entry)
        link = m.get_upload_link(file)

        # TODO: Create text file of links
        print(link)


if __name__ == "__main__":
    main()
