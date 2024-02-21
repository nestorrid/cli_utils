# -*- coding: utf-8 -*-
# @File    :   pyheader
# @Time    :   2024-02-21 17:29:48
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" Header for python files """

from typing import Iterable
from datetime import datetime

from .base import BaseFileHeader
from nescli import config


class PythonFileHeader(BaseFileHeader):

    def generate(self, path: str) -> Iterable[str]:
        if not config.get('add_header'):
            return []

        paths = path.rsplit('/', 2)

        header = [
            "# -*- coding: utf-8 -*-\n",
            f"# @File    :   {paths[1]}/{paths[2]}\n",
            f"# @Time    :   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        ]

        if self.config.get('user'):
            header.append(f"# @Author  :   {self.config.get('user')}\n")
        if self.config.get('email'):
            header.append(f"# @Email   :   {self.config.get('email')}\n")

        header.append('\n""" docstring """')

        return header
