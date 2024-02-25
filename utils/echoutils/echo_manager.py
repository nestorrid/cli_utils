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

from utils.strutil import TabChar, print_length, str_to_lines

from .builder import CliTableBuilder, EchoBuilder


@dataclass(eq=False, order=False)
class EchoStatment:

    """
    This class is use to print multiple statements in a single line.
    """

    msg: str
    fg: t.Optional[str] = field(default=None, repr=False)
    bg: t.Optional[str] = field(default='reset', repr=False)
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

    def end(self, *, with_prefix: t.Union[bool, str] = '>>'):

        if with_prefix:
            self.prefix(with_prefix)
        else:
            self.prefix('')

        if len(self.__attachs) > 0:
            self.__attachs[-1]._nl = True
        else:
            self._nl = True

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

    max_length = 100

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
        self.print_sep(print_length(_title))

    def _get_prefix(self, prefix: str = None, show_prefix: bool = None):

        if show_prefix is None:
            if self.show_prefix:
                return (prefix or self.prefix) + ' '

        if show_prefix:
            return (prefix or self.prefix) + ' '

        return ""

    def done(self):
        self.__echo('Done!', show_prefix=False)

    def confirm_delete(self, msg: str):
        _type = 'Key' if '/' in msg else 'Path'
        return self.confirm(f'Do you want to delete {_type}: {msg!r}?')

    def confirm_replace(self, key, value):
        prompt = f'Key `{key}` is already set to `{value}`. Do you want to replace it?'
        return self.confirm(prompt)

    def confirm_replace_file(self, path):
        prompt = f'{path!r} is already exists. Do you want to overwrite it?'
        return self.confirm(prompt)

    def confirm(self, msg: str):
        self.__echo(msg + '[y/N]: ', fg=self.color_blue, nl=False)
        result = input()
        return len(result) == 0 or result.lower() == 'y'

    def copy(self, src, dest):
        es('copy: ').add(
            es(src).magenta.bold.underline
        ).end()

        es('to:   ').add(
            es(dest).magenta.bold.underline
        ).end()

    def not_found(self, target):
        es('Target: ').add(
            es(target).magenta.bold.underline
        ).add(' is not found.').end()

    def remove_key(self, key):
        es('Key: ').add(
            es(key).magenta.bold.underline
        ).add(' is removed.').end()

    def remove_file(self, file):
        es('File: ').add(
            es(key).magenta.bold.underline
        ).add(' is removed.').end()

    def statments(self, *stmts: t.Iterable[t.Union[str, EchoStatment]], with_prefix='>>'):
        start = stmts[0] if isinstance(
            stmts[0], EchoStatment) else es(stmts[0])

        if len(stmts) > 1:
            for stmt in stmts[1:]:
                start.add(stmt)

        start.end(with_prefix=with_prefix)

    def _adjust_column_width(self, col_width: t.Iterable[int]):
        line_width = reduce(lambda x, y: x + y, col_width)
        max_width = max(col_width)
        if line_width > self.max_length:
            widths = [w if w < max_width else w - 4 for w in col_width]
            return self._adjust_column_width(widths)

        return col_width

    def table(
            self, lines: t.Iterable[t.Iterable[str]],
            first_line_as_header: bool = True,
    ):
        columns = len(lines[0])

        wrong_column_lines = list(filter(lambda x: len(x) != columns, lines))

        if len(wrong_column_lines) > 0:
            raise ValueError(
                f'Columns must be {columns!r}, but line {wrong_column_lines!r} got {len(wrong_column_lines)!r}.')

        column_length = self._adjust_column_width([
            max([print_length(line[i]) for line in lines]) + 2
            for i in range(columns)
        ])

        if first_line_as_header:
            self._echo_table_header(
                line=lines[0], col_width=column_length)
            lines = lines[1:]

        for line in lines:
            self._echo_table_line(line, col_width=column_length)

        self._echo_table_bottom_line(column_length)

    def _adjust_line_width(self, line: t.Iterable[str], col_width: t.Iterable[int]) -> t.Iterable[t.Iterable[str]]:
        columns = list(zip(line, col_width))

        results = []

        for column in columns:
            lines = str_to_lines(column[0], column[1] - 2)
            results.append(lines)

        line_count = max([len(l) for l in results])
        for line in results:
            while len(line) < line_count:
                line.append('')

        lines = [
            [col[i] for col in results]
            for i in range(line_count)
        ]

        return lines

    def _echo_table_header(self, line: t.Iterable[str], col_width: t.Iterable[int]):

        columns = [es(TabChar.CORNER_TOP_LEFT)]
        for w in col_width[:-1]:
            columns.append(
                es(TabChar.INDENT * (w - 1) + TabChar.BRANCH_TOP)
            )
        columns.append(es(
            TabChar.INDENT * (col_width[-1] - 1) + TabChar.CORNER_TOP_RIGHT))
        self.statments(*columns, with_prefix=False)

        columns = [es(TabChar.PIPE)]
        for idx, col in enumerate(line):
            spaces = (col_width[idx] - print_length(col) - 1) * ' '
            columns.append(es(f'{col}{spaces}{TabChar.PIPE}').blue.bold)
        self.statments(*columns, with_prefix=False)

        columns = [es(TabChar.BRANCH_LEFT)]
        for w in col_width[:-1]:
            columns.append(
                es(TabChar.INDENT * (w - 1) + TabChar.CROSS)
            )
        columns.append(es(
            TabChar.INDENT * (col_width[-1] - 1) + TabChar.BRANCH_RIGHT))
        self.statments(*columns, with_prefix=False)

    def _echo_table_line(self, line: t.Iterable[str], col_width: t.Iterable[int],):

        lines = self._adjust_line_width(line, col_width)

        if len(lines) > 1:
            for line in lines:
                self._echo_table_line(line, col_width)
            return

        columns = [es(TabChar.PIPE)]
        for idx, col in enumerate(line):
            spaces = (col_width[idx] - print_length(col) - 1) * ' '
            columns.append(es(f'{col}{spaces}{TabChar.PIPE}'))
        self.statments(*columns, with_prefix=False)

    def _echo_table_bottom_line(self, col_width: t.Iterable[int]):

        columns = [es(TabChar.CORNER_BOTTOM_LEFT)]
        for w in col_width[:-1]:
            columns.append(
                es(TabChar.INDENT * (w - 1) + TabChar.BRANCH_BOTTOM)
            )
        columns.append(es(
            TabChar.INDENT * (col_width[-1] - 1) + TabChar.CORNER_BOTTOM_RIGHT))
        self.statments(*columns, with_prefix=False)


echo = EchoManager()
es = EchoStatment
