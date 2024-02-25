# -*- coding: utf-8 -*-
# @File    :   builder/cli_table.py
# @Time    :   2024-02-25 11:50:36
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" docstring """

from .base import EchoBuilder


class CliTableBuilder(EchoBuilder):

    def echo(self, first_line_as_header=True):
        print('table')
