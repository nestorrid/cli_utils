# -*- coding: utf-8 -*-
# @File    :   file_util
# @Time    :   2024-02-20 21:19:37
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" basic functions for file and folder operations """

from typing import Iterable
import os

import click

from .message import msgbox
from nescli.core.headers import python_header


def copy(src: str, dest: str, safe: bool = False):
    """
    Copy src file to the dest.

    Args:

        :param str src: full path to the source file.
        :param str dest: full path to the destination file.
        :param bool safe: check source file and dest path before action, by default False, defaults to False

    Raises:

        :raises FileExistsError: Raise if destination file is exists and safe is True.
        :raises FileNotFoundError: Raise if source file is not found and safe is True.
    """

    if safe:
        if os.path.exists(dest):
            raise FileExistsError(f'{dest!r} is already exists.')

        if not os.path.exists(src):
            raise FileNotFoundError(f'{src!r} is not found.')

    if os.path.exists(dest):
        os.remove(dest)

    with open(src, 'r') as src:
        with open(dest, 'a') as dst:
            dst.writelines(src.readlines())


def create_folder(path: str):
    """
    Create folder in the given path. Will push a result message to the `msgbox`.

    :ref:`util-Message`

    Parameters
    ----------
    path : str
        full path to the folder.

    """
    try:
        os.mkdir(path)
        msgbox.push(f'> Create folder {path!r}.')
    except FileExistsError as err:
        msgbox.push(f'> Target folder {path!r} is already exists.')
    except FileNotFoundError:
        if click.confirm(
            f'Parent folder for {os.path.basename(path)!r} is not exists.\n'
            'Do you want to create path to it?'
        ):
            os.makedirs(path)
            msgbox.push(f'> Create path to {path!r}.')


def create_python_file(path: str):
    """
    Create a python file for the given path.

    Parameters
    ----------
    path : str
        Full path to the python file. With or without extension.
    """

    if not path.endswith('.py'):
        path += '.py'

    create_file(path, header=python_header.generate(path))


def create_file(path, name=None, /, header: Iterable = None):
    """
    Create file at the given path.

    After creating the file, a successful message will push to `msgbox`.

    You can use `utils.msgbox.echo()` to print this message to the console.

    :ref:`utils-Message`.

    Parameters
    ----------
    path : str
        Full path or base path of the file.
    name : str, optional
        Only set this when using base path. defaults to None.

        for example:

            create_file('some/path/to', 'file')

    header : Iterable, optional
        Contents for the file's header, normally mata info or comments.
        defaults to None
    """
    if name:
        path = os.path.join(path, name)

    if os.path.exists(path):
        msgbox.push(f'> File {path!r} is already exists.')
        return

    pwd = os.path.dirname(path)
    if not os.path.exists(pwd):

        if click.confirm(f'{pwd!r} is not exists. \nWould you like to create it?', default=True):
            os.makedirs(pwd)
            msgbox.push(f'> Create path to{pwd!r}.')
        else:
            msgbox.push(f'> Cancel creating {path!r}.')
            return

    if header:
        with open(path, 'w') as f:
            for line in header:
                f.write(line)

    msgbox.push(f'> Create file: {path}.')
