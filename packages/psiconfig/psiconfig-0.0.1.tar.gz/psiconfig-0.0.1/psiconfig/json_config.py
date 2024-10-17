"""Return a config object from a json file for the application."""

import json

from .config import Config
from .constants import STATUS
from .text import INVALID_JSON, DEFAULTS_ERR


class JsonConfig(Config):
    """
        A class to handle config files in json format
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_config(self) -> dict[str, object]:
        """Open the config file and return the contents as a dict."""
        self.status = STATUS['ok']
        try:
            with open(self.path, 'r') as f_config:
                try:
                    config = json.load(f_config)
                    return self.check_defaults(config)
                except json.decoder.JSONDecodeError:
                    if self.defaults:
                        return self.defaults
                    else:
                        self.error = f'{INVALID_JSON} {self.path}'
        except FileNotFoundError:
            if self.defaults:
                return self.defaults
            else:
                self.error = DEFAULTS_ERR
        self.status = STATUS['error']
        return {}

    def save(self):
        if not self.path.parent.is_dir():
            self.create_directories()
        try:
            with open(self.path, 'w') as f_config:
                json.dump(self.__dict__['config'], f_config)
            return STATUS['ok']
        except Exception as err:
            self.status = STATUS['error']
            self.error = err
