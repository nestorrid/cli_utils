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
            msgbox.push(f'> Create path {pwd!r}.')
        else:
            msgbox.push(f'> Cancel creating {path!r}.')
            return

    with open(path, 'w') as f:
        for line in header:
            f.write(line)

    msgbox.push(f'> Create file: {path}.')
