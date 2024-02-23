# -*- coding: utf-8 -*-
# @File    :   conf_manage
# @Time    :   2024-02-23 16:52:28
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" Configuration file management """

import click

from utils import es


@click.group()
def confcli():
    """
    conf command is use to manage configuration files.
    """
    pass


@confcli.command()
def set():

    es('test ').cyan.bold.add(
        es('stmt').magenta.underline.add(' ')
    ).add(
        es('text').white.red_bg
    ).end(with_prefix='>>')


@confcli.command()
def edit():
    pass


@confcli.command('rm')
def remove():
    pass


@confcli.command()
def use():
    pass
