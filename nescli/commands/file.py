# -*- coding: utf-8 -*-
# @File    :   file
# @Time    :   2024-02-20 15:30:56
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" CLI Command to create files. """

import os
from typing import Iterable

import click

from utils import echo, msgbox, futil
from nescli import config
from nescli.core.headers import python_header


@click.group()
def cli():
    pass


def _find_tests_directory(path=None):

    if path == '/':
        return None

    if not path:
        path = os.path.abspath('.')

    tp = os.path.join(path, 'tests')

    if not os.path.exists(tp):
        return _find_tests_directory(os.path.dirname(path))

    return tp


def _create_test_file(names):
    tests_path = _find_tests_directory()
    if not tests_path:
        return None

    header = [
        "try:\n",
        "\timport pytest\n",
        "except ImportError:\n",
        "\timport unittest\n",
    ]

    for name in names:
        full_path = os.path.join(tests_path, name)
        if not os.path.exists(full_path):
            futil.create_file(
                os.path.dirname(full_path),
                f'test_{os.path.basename(full_path)}.py',
                header=header)


@cli.command('py')
@click.argument('names', nargs=-1)
@click.option('-v', '--verbose', is_flag=True, help='Show information details.')
@click.option(
    '-t', '--test', 'is_test',
    is_flag=True,
    help="""
    Create test files which will starts with `test_`. 
    
    \b
    For example:
        f py demo -t
    Will create a `test_demo.py` file under the `tests` directory.
    
    At first, this command will search the `tests` directory in the current path.
    If no `tests` directory is found, it will search the parent paths until `tests` folder is found or no more parent path.
    """)
@click.option(
    '-p', '--path', 'basepath',
    default=None,
    help="""
    Setup a base path for once. All files will be created under the given base path.
    
    By default, base path is relative to the current working directory. For example:

        -p subpath
            equivalent to -p ./subpath
    
    If the base path is start with `/`, it will be treated as absolute path.
    """
)
def create_py_files(names, verbose, is_test, basepath):
    """
    Create multiple python files under current directory.

    NAMES

        Names for python file, separated by space. Extension name is unnecessary. 

        For example: `f py app demo`
    """

    if len(names) == 0:
        echo("At least one name is required.", show_prefix=True)
        return

    if is_test:
        _create_test_file(names)
    else:
        _create_files(names, basepath)

    if verbose:
        msgbox.echo(verbose=verbose)

    echo('Done!')


def _is_absolute_path(path):
    return path.startswith('/')


def _create_files(names: Iterable[str], basepath: str):
    if not basepath:
        basepath = os.path.abspath('.')
    else:
        if not _is_absolute_path(basepath):
            basepath = '' if basepath.startswith('./') else './' + basepath

    for name in names:
        futil.create_python_file(os.path.join(basepath, name))
