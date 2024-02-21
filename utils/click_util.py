# -*- coding: utf-8 -*-
# @File    :   click_util
# @Time    :   2024-02-20 15:43:35
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" util functions for click """


import click


def echo(msg=None, fg='yellow', show_prefix=False, prefix='>>', nl=True):

    if not msg:
        click.echo(click.style('='*40, fg=fg))
        return

    if show_prefix:
        msg = prefix + " " + msg
    click.echo(click.style(msg, fg=fg), nl=nl)
