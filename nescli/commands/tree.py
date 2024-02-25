# -*- coding: utf-8 -*-
# @File    :   utils
# @Time    :   2024-02-18 19:39:10
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" 
    Print the file structure of the given directory.
"""


import os
import sys
from collections import namedtuple
from typing import List

from click import (
    command,
    option,
    argument,
    group,
    style
)

import click

from utils.strutil import TabChar
from utils import echo
from nescli import config

Line = namedtuple('Line', ['content', 'fg'], defaults=["", 'white'])

# config = dict(

#     show_hidden=False,
#     max_depth=8
# )


@command()
@option('-d', '--depth',
        default=8,
        help='The recursion depth to show. Set depth to `0` will show all sub directory contents under the target.',
        show_default=True)
@option('-h/-H', 'show_hidden',
        help='Show hidden files, default is False.')
@argument('target', default='.')
def tree(depth, target, show_hidden):
    """
        Print the file structure for the target directory which will be current directory by default.

        Arguments:

        TARGET  
            The path to show, default is the current directory. This arg can not be file.
    """
    abspath = os.path.abspath(target)

    if not _is_directory(abspath):
        raise click.BadParameter(
            f'Target must be a directory. But got a file: {abspath!r}')

    config.set('show_hidden', show_hidden)
    config.set('max_depth', depth)
    config.set('indent', 2)
    config.set('indent_char', TabChar.INDENT)

    result = _format_sublines(_print_structure(abspath))

    if len(result) == 0:
        echo(f'Target directory {abspath!r} is empty.', fg='red')
        return

    echo.print_title(f"Structure for path {abspath!r}")
    echo(
        TabChar.CORNER_TOP_LEFT + abspath.split('/')[-1],
        fg='blue', show_prefix=False)

    for line in result:
        echo(line.content, fg=line.fg, show_prefix=False)


def _print_structure(path, depth=0) -> List[Line]:

    if depth > config.get('max_depth') > 0:
        return []

    if _is_file(path):

        if depth == 0:
            raise click.BadParameter(
                f'tree can only show the structure of directories, but got file {path}')

        return [Line(TabChar.INDENT + path.split('/')[-1])]

    contents = _filtered_contents(path)

    if len(contents) == 0:
        return []

    lines = []

    for i, content in enumerate(contents):

        prefix = TabChar.INDENT
        fg = 'white'
        content_path = os.path.join(path, content)
        sublines = []
        is_last_directory = False
        if _is_directory(content_path):
            fg = 'blue'
            if i == len(contents) - 1:
                is_last_directory = True

            sublines = _print_structure(content_path, depth=depth+1)
            if len(sublines) > 0:
                prefix = TabChar.BRANCH_TOP

            lines.append(Line(prefix + content, fg=fg))
            lines += _format_sublines(sublines)
        else:
            lines.append(Line(prefix + content, fg=fg))

    return lines


def _format_sublines(sublines):
    lines = []
    for j, subline in enumerate(sublines):
        content = subline.content
        if _is_child_for_current_directory(content):
            prefix = TabChar.BRANCH_LEFT + TabChar.INDENT
            if j == len(sublines) - 1:
                prefix = TabChar.CORNER_BOTTOM_LEFT + TabChar.INDENT
        else:
            prefix = TabChar.PIPE + " "
        lines.append(Line(prefix + content, fg=subline.fg))

    return _remove_detached_pipes(lines)


def _remove_detached_pipes(lines):

    if len(lines) == 0:
        return lines

    has_detached_pipes = lines[-1].content.startswith(TabChar.PIPE)

    if not has_detached_pipes:
        return lines

    formatted_lines = []

    for line in reversed(lines):

        if has_detached_pipes and line.content.startswith(TabChar.PIPE):
            formatted_lines.append(
                Line(' ' + line.content[1:], fg=line.fg)
            )
            continue

        has_detached_pipes = False
        formatted_lines.append(line)

    return list(reversed(formatted_lines))


def _is_child_for_current_directory(content):
    return content.startswith(TabChar.INDENT) or content.startswith(TabChar.BRANCH_TOP)


def _is_python_cache(name):
    return name.startswith('__') and name.endswith('__')


def _filtered_contents(path):
    contents = os.listdir(path)

    if not config.get('show_hidden'):
        contents = list(filter(lambda x: not x.startswith('.') and not (
            x.startswith('__') and x.endswith('__')), contents))

    return contents


def _build_line(line: Line, depth):
    content = line.content
    if content.startswith(TabChar.INDENT) or content.startswith(TabChar.BRANCH_TOP):
        content = (
            TabChar.BRANCH_LEFT +
            config['indent_char'] +
            content)

    return click.style(content, fg=line.fg)


def _is_directory(path):
    return os.path.isdir(path)


def _is_file(path):
    return os.path.isfile(path)
