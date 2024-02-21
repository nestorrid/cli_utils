# -*- coding: utf-8 -*-
# @File    :   sysutil
# @Time    :   2024-02-18 19:30:19
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" 
    A util command set for system  

    This library is developed under Mac OS. Untested for other platforms.
"""


from click import (
    command,
    option,
    argument,
    group,
    echo,
    style
)

import click


@group('sys')
def util():
    pass


@util.command()
@option('--paths', envvar='PATH', type=click.Path(), multiple=True)
def paths(paths):
    """
    Print the paths in the PATH environment variable.
    """
    for path in paths:
        echo(path)


if __name__ == "__main__":
    util()
