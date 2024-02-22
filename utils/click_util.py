# -*- coding: utf-8 -*-
# @File    :   click_util
# @Time    :   2024-02-20 15:43:35
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" util functions for click """

from dataclasses import dataclass
from functools import reduce
import typing as t
import click


@dataclass
class EchoManager():

    show_prefix: bool = True
    prefix: str = '>> '
    nl: bool = True
    fg: str = 'yellow'
    bg: str = 'reset'
    bold: bool = False
    underline: bool = False
    sep_length: int = 60
    sep_char: str = '='
    title: str = 'Message:'

    color_black = 'black'
    color_red = 'red'
    color_green = 'green'
    color_yellow = 'yellow'
    color_blue = 'blue'
    color_magenta = 'magenta'
    color_cyan = 'cyan'
    color_white = 'white'

    def __call__(
        self, msg: str = None,
        fg: t.Optional[t.Union[int, t.Tuple[int, int, int], str]] = None,
        bg: t.Optional[t.Union[int, t.Tuple[int, int, int], str]] = None,
        show_prefix: bool = None, prefix: str = None,
        bold: bool = None, underline: bool = None,
        nl: bool = None
    ):

        self.__echo(
            msg, fg=fg, show_prefix=show_prefix,
            prefix=prefix, nl=nl, bold=bold, underline=underline, bg=bg)

    def __echo(
            self, msg, /,
            fg=None, bg=None,
            prefix=None, show_prefix=None,
            bold=None, underline=None,
            nl=None
    ):

        if msg is None:
            self.print_sep()
            return

        _prefix = self._get_prefix(prefix, show_prefix)
        msg = _prefix + msg

        styled = click.style(
            msg,
            fg=fg or self.fg,
            bg=bg or self.bg,
            bold=bold if bold is not None else self.bold,
            underline=underline if underline is not None else self.underline
        )

        click.echo(styled, nl=nl if nl is not None else self.nl)

    def print_sep(self, length: int = None, separator: str = None):
        _len = length or self.sep_length
        _sep = separator or self.sep_char
        self.__echo(_sep * _len, show_prefix=False)

    def print_title(self, title: str = None):
        _title = title or self.title
        self.__echo(_title, show_prefix=False)
        self.print_sep()

    def _get_prefix(self, prefix: str = None, show_prefix: bool = None):

        if show_prefix is None:
            if self.show_prefix:
                return prefix or self.prefix

        if show_prefix:
            return prefix or self.prefix

        return ""

    def done(self):
        self.__echo('Done!', show_prefix=False)

    def confirm(self, msg: str):
        self.__echo(msg + '[y/N]: ', fg=self.color_magenta, nl=False)
        result = input()
        return len(result) == 0 or result.lower() == 'y'


echo = EchoManager()
