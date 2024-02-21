# -*- coding: utf-8 -*-
# @File    :   base
# @Time    :   2024-02-21 17:25:40
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" Basic File Header """

from typing import Iterable
from nescli.core.config import CLIConfig


class BaseFileHeader:

    def __init__(self, config: CLIConfig = None):
        self.config = config

    def generate(self, path: str) -> Iterable[str]:
        raise NotImplementedError(
            "Subclass of BaseFileHeader should implement this method.\n"
            "Return a list of headers text.")
