# -*- coding: utf-8 -*-
# @File    :   click_util
# @Time    :   2024-02-20 15:43:35
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" util functions for click """

from __future__ import annotations

from dataclasses import dataclass, field
from functools import reduce
import typing as t
import click


@dataclass(eq=False, order=False)
class EchoStatment:

    """
    This class is use to print multiple statements in a single line.
    """

    msg: str
    fg: t.Optional[str] = field(default=None, repr=False)
    bg: t.Optional[str] = field(default=None, repr=False)
    _bold: t.Optional[bool] = field(default=False, repr=False)
    _underline: t.Optional[bool] = field(default=False, repr=False)
    _nl: t.Optional[bool] = field(default=False, repr=False)
    _prefix: t.Optional[str] = field(default='', repr=False)

    __attachs: list[EchoStatment] = field(
        default_factory=list, init=False, repr=False, compare=False)
    _start_stmt: EchoStatment = field(
        default=None, init=False, repr=False, compare=False)

    # def __str__(self):
    #     return self.msg

    # def __repr__(self):
    #     return self.msg

    def prefix(self, prefix=''):
        self._prefix = prefix
        return self

    def __eq__(self, other):
        return id(self) == id(other)

    def add(self, stmt: t.Union[EchoStatment, str]):
        if isinstance(stmt, str):
            stmt = EchoStatment(stmt)
        self.__attachs.append(stmt)
        return self

    def end(self, *, with_prefix=''):
        self.prefix(with_prefix)
        self.__attachs[-1]._nl = True
        self._echo()
        return self

    def _echo(self):
        echo(
            self.msg,
            fg=self.fg, bg=self.bg,
            show_prefix=self._prefix, prefix=self._prefix,
            bold=self._bold, underline=self._underline, nl=self._nl
        )

        for stmt in self.__attachs:
            stmt._echo()

    @property
    def bold(self):
        self._bold = True
        return self

    @property
    def underline(self):
        self._underline = True
        return self

    @property
    def white(self):
        self.fg = 'white'
        return self

    @property
    def white_bg(self):
        self.bg = 'white'
        return self

    @property
    def cyan(self):
        self.fg = 'cyan'
        return self

    @property
    def cyan_bg(self):
        self.bg = 'cyan'
        return self

    @property
    def magenta(self):
        self.fg = 'magenta'
        return self

    @property
    def magenta_bg(self):
        self.bg = 'magenta'
        return self

    @property
    def green(self):
        self.fg = 'green'
        return self

    @property
    def green_bg(self):
        self.bg = 'green'
        return self

    @property
    def red(self):
        self.fg = 'red'
        return self

    @property
    def red_bg(self):
        self.bg = 'red'
        return self

    @property
    def yellow(self):
        self.fg = 'yellow'
        return self

    @property
    def yellow_bg(self):
        self.bg = 'yellow'
        return self

    @property
    def blue(self):
        self.fg = 'blue'
        return self

    @property
    def blue_bg(self):
        self.bg = 'blue'
        return self

    @property
    def black(self):
        self.fg = 'black'
        return self

    @property
    def black_bg(self):
        self.bg = 'black'
        return self


@dataclass
class EchoManager():

    show_prefix: bool = True
    prefix: str = '>>'
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

    def __echo_statements(self, stmts):
        print('echo statements')

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
                return (prefix or self.prefix) + ' '

        if show_prefix:
            return (prefix or self.prefix) + ' '

        return ""

    def done(self):
        self.__echo('Done!', show_prefix=False)

    def confirm(self, msg: str):
        self.__echo(msg + '[y/N]: ', fg=self.color_magenta, nl=False)
        result = input()
        return len(result) == 0 or result.lower() == 'y'


echo = EchoManager()
es = EchoStatment
