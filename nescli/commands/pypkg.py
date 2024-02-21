# -*- coding: utf-8 -*-
# @File    :   pypkg
# @Time    :   2024-02-19 16:24:21
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" 
    This command is for create python packages easily in vscode.
"""

import os
import json
from pathlib import Path
from datetime import datetime

import click

from utils import echo, msgbox
from nescli import config
from nescli.core.headers import python_header

KEY_USER = 'user'
KEY_MAIL = 'email'
KEY_ADD_HEADER = 'add_header'


def setup_project_basic_packages(ctx, param, value):

    if not value:
        return

    path = os.path.abspath('.')
    folder = path.rsplit('/', 1)[1]
    _create_packages(path, folder)
    _create_packages(path, 'tests')
    _create_file(os.path.join(path, 'app.py'))

    msgbox.echo(verbose=True)

    ctx.exit()


def show_config_info(ctx, param, value):
    if not value:
        return

    echo("CONFIG INFO:", show_prefix=True)
    echo()
    for key in config.keys():
        echo(f'{key}: {config.get(key)}')

    ctx.exit()


def set_user(ctx, param, value):

    if not value:
        return

    config.set(KEY_USER, value)
    echo(f'USERNAME is set to {value!r}')
    ctx.exit()


def set_mail(ctx, param, value):

    if not value:
        return

    config.set(KEY_MAIL, value)
    echo(f'EMAIL is set to {value!r}')
    ctx.exit()


def set_show_header(ctx, param, value):

    if config.get(KEY_ADD_HEADER) == value:
        return

    config.set(KEY_ADD_HEADER, value)
    echo(f'Package init file header is {"ON" if value else "OFF"}')
    ctx.exit()


@click.command()
@click.argument('names', nargs=-1)
@click.option(
    '-p', '--path', 'is_path',
    is_flag=True,
    help="""
        Path flag. 
        With this flag, you need to give the full path to the package. 
        Wildcards can be used, like `./somepackage/newpackage`
        """)
@click.option(
    '-v', '--verbose', is_flag=True,
    help='Add this flag to show full log messages.')
@click.option(
    '-i', '--info',
    is_flag=True,
    default=False,
    expose_value=False,
    callback=show_config_info,
    help='Show `user` and `mail` info. It will be used in the `__init__.py` file\'s header.')
@click.option(
    '-u', '--user',
    help='The username which will be shown in the `__init__.py` file\'s header. You can use `--setuser` to set the username globally.',
    expose_value=False, callback=set_user)
@click.option(
    '-m', '--mail',
    help='The mail address which will be shown in the `__init__.py` file\'s header. You can use `--setmail` to set the username globally.',
    expose_value=False, callback=set_mail)
@click.option(
    '-h/-H', expose_value=False,
    default=True,
    show_default=True,
    callback=set_show_header,
    help='Add file header in `__init__.py` file. If you don\'t want to add any thing run `pkg -H` to close it.')
@click.option(
    '-s', '--setup', is_flag=True, expose_value=False,
    callback=setup_project_basic_packages,
    help="""
    Setup a basic python project structure.
    The structure will like this:
    
    \b
    project
    |--project
    | |-__init__.py
    |--tests
    | |-__init__.py
    |--app.py
    """
)
def pkg(names, is_path, verbose):
    """
    Quickly create python packages.

    This command will check for the package existence. If not, it will create a folder with the given name
    and a `__init__.py` file inside.

    You can create nested packages by passing a absolute or relative path.
    For example:

        `pkg -a ./project/core`

    This command will create package `core` under `project`.
    If directory `project` is not exists, it will be created automatically, and turn into package.

    Args:

        names (str): The name of package. Can be multiple names separated by space.
    """

    for name in names:
        path, pkg, target = _parse_package(name, is_path)
        if os.path.exists(target):
            if not _directory_is_package(target):
                _convert_directory_to_package(target)
        else:
            _create_packages(path, pkg)

    if verbose:
        msgbox.echo(verbose=verbose)

    echo('Done!')


def _create_folder(path):
    try:
        os.mkdir(path)
        msgbox.push(f'> Create folder {path!r}.')
    except FileExistsError as err:
        msgbox.push(f'> Target folder {path!r} is already exists.')


def _create_packages(path, pkg):

    if not os.path.exists(path):
        p, t = path.rsplit('/', 1)
        _create_packages(p, t)

    msgbox.push(f'- NEW PACKAGE: {pkg}')
    target = os.path.join(path, pkg)
    _create_folder(target)
    _convert_directory_to_package(target)
    msgbox.push(f'> New package {pkg!r} is created.\n')


def _convert_directory_to_package(path):
    if not _directory_is_package(path):
        _create_file(os.path.join(path, '__init__.py'))
        msgbox.push(f'> Directory {path!r} is converted to package.')


def _create_file(path):

    if os.path.exists(path):
        msgbox.push(f'> File {path!r} is already exists.')
        return

    headers = python_header.generate(path)

    with open(path, 'w') as f:
        for line in headers:
            f.write(line)

    msgbox.push(f'> Create file: {path}.')


def _directory_is_package(target):
    if os.path.exists(os.path.join(target, '__init__.py')):
        msgbox.push(
            f'> Package {target!r} is already exists.')
        return True


def _parse_package(name, is_path):
    if is_path:
        path, pkg = name.rsplit('/', 1)
        path = os.path.abspath(path)
    else:
        if '/' in name:
            raise click.BadParameter(
                """\n>> Package name can not contain `/`, use option `-p` to create packages with full path.""")
        path = os.path.abspath('.')
        pkg = name

    return path, pkg, os.path.join(path, pkg)
