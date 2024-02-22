# -*- coding: utf-8 -*-
# @File    :   config
# @Time    :   2024-02-20 22:23:22
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" Configuration Management """

import os
import json
from pathlib import Path
from typing import Dict

default_config = dict(
    user='undefined',
    email='undefined',
    add_header=True,
)


class CLIConfig:

    def __init__(self, path=None):
        self._path = path or os.path.join(
            os.environ.get('HOME'), '.nescli.conf')
        self._conf = self._load_config()

    def _load_config(self) -> Dict:
        """
        Load config object from the given path.

        If no path is provided, the config file will be stored in `~/.nescli.conf`.

        Returns
        -------
        Dict
            Config object.
        """
        if os.path.exists(self._path):
            return json.loads(Path(self._path).read_text())

        return default_config

    def get(self, key: str) -> str | None:
        """
        read string value from config file. None if the key is not found.
        """
        return self._conf.get(key, None)

    def set(self, key: str, value):
        """
        set new key value pair to the config file.
        """
        self._conf[key] = value
        self._write_config()

    def _write_config(self):
        with open(self._path, 'w') as f:
            f.write(json.dumps(self._conf))

    def remove(self, key: str):
        del self._conf[key]
        self._write_config()

    @property
    def keys(self):
        return self._conf.keys()


config = CLIConfig()
