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


def main():
    config = get_config()

    mega = Mega()
    m = mega.login(config["email"], config["password"])

    details = m.get_user()
    print(details)

if __name__ == "__main__":
    main()
