# -*- coding: utf-8 -*-
# @File    :   conf_manage
# @Time    :   2024-02-23 16:52:28
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" Configuration file management """

import os
import sys
import functools
from collections import namedtuple
from pathlib import Path

import click

from utils import es, msgbox, echo, futil
from nescli import config

KEY_CONFIG_TEMPLATES = 'config_templates'

Template = namedtuple('Template', ['name', 'desc'])


def _template_folder():
    return os.path.join(os.environ['HOME'], '.nescli_conf_templates')


def _check_conf_template_folder():
    return os.path.exists(_template_folder())


if not _check_conf_template_folder():
    os.mkdir(_template_folder())


def _vscode_is_available():
    out = os.popen('type code')
    return 'not found' not in out.read()


def use_config(func):
    confs = config.get(KEY_CONFIG_TEMPLATES, {})

    @functools.wraps(func)
    def inner(*args, **kwargs):
        confs = config.get(KEY_CONFIG_TEMPLATES, {})
        kwargs.setdefault('confs', confs)
        result = func(*args, **kwargs)
        config.set(KEY_CONFIG_TEMPLATES, confs)
        return result

    return inner


@use_config
def _set_template(key: str, name: str, desc: str = None, edit: bool = True, ** kwargs):

    old = _get_template(key, _echo=False)
    basename = os.path.basename(name)

    if old:
        if old == [basename, desc] or not echo.confirm_replace(key, old):
            return

    confs = kwargs.get('confs')
    confs[key] = [basename, desc]

    echo.statments(
        'Set template: ',
        es(basename).magenta.bold.underline,
        ' for key: ',
        es(key).magenta.bold.underline
    )

    if desc:
        echo.statments(
            'Description: ',
            es(desc).magenta.underline
        )

    if edit:
        _edit_template_file(basename)
    else:
        futil.copy(name, os.path.join(_template_folder(), basename))

    return True


@use_config
def _get_template(key, _echo=True, **kwargs) -> Template:
    value = kwargs.get('confs').get(key, None)

    if not value:
        if _echo:
            echo.not_found(key)
        return

    return Template(value[0], value[1])


@use_config
def _update_template_desc(key, desc, **kwargs):
    confs = kwargs.get('confs')
    confs[key][1] = desc
    echo.statments(
        'Description for key: ',
        es(key).magenta.bold.underline,
        ' is set to: ',
        es(desc).magenta.bold.underline
    )


@use_config
def _remove_template(key, **kwargs):

    template = _get_template(key)

    if not template:
        return

    temp_file = os.path.join(_template_folder(), template.name)
    if os.path.exists(temp_file):
        os.remove(temp_file)

    confs = kwargs.get('confs')
    del confs[key]

    echo.remove_key(key)


def _edit_template_file(name):

    template_file = os.path.join(_template_folder(), name)

    if not os.path.exists(template_file):
        futil.create_file(template_file)

    cmd = 'code ' if _vscode_is_available() else 'open '
    cmd += template_file

    os.popen(cmd)


@click.group()
def confcli():
    """
    conf command is use to manage configuration files.
    """
    pass


@confcli.command()
@click.argument('key', metavar='<KEY>')
@click.argument('name', metavar='<NAME>')
@click.argument('desc', required=False)
def add(key, name, desc):
    """
    Add a config file to template folder.

    Similar to `save` command, but this command will create an empty file in the template folder.
    Then open it for you for further editing.

    key : str
        Shortcut for the config file.

    name : str
        Name of the config file.

    desc : str
        Description of the config file.
    """

    _set_template(key, name, desc)
    echo.done()


@confcli.command()
@click.argument('key')
@click.option('-d', '--desc', help='Edit description for key.')
def edit(key, desc):
    """
    Edit template file.

    key : _type_
        Key for the template file.
    """

    template = _get_template(key)

    if not template:
        return

    if desc:
        _update_template_desc(key, desc)
        return

    _edit_template_file(template.name)
    echo.done()


@confcli.command('rm')
@click.argument('key')
def remove(key):
    """
    Remove temporary file.

    key : str
        Key for the temporary file.
    """
    template = _get_template(key)

    if not template:
        return

    if echo.confirm_delete(key):
        _remove_template(key)

    echo.done()


@confcli.command()
@click.argument('key')
@click.argument('path', default='.')
def use(key, path):
    """
    Copy config file from template folder to target path.

    key : str
        Key for the config file.

    path: str
        Path to save config file. Default is current working directory.
    """
    template = _get_template(key)

    if not template:
        return

    template_file = os.path.join(_template_folder(), template.name)

    if not os.path.exists(template_file):
        echo.not_found(template.name)
        return

    if os.path.exists(os.path.join(path, template.name)):
        if not echo.confirm_replace_file(os.path.join(path, template.name)):
            return

    echo.copy(
        template_file,
        os.path.join(path, template.name)
    )

    futil.copy(template_file, os.path.join(path, template.name))

    echo.done()


@confcli.command('list')
def list_confs():
    confs = config.get(KEY_CONFIG_TEMPLATES, {})

    if len(confs) == 0:
        echo('No configuration. Use `conf add` to create configurations.')
        return

    echo.print_title('Cached configurations')
    data = [['KEY', 'FILE NAME', 'DESC']]
    data += [[key, confs[key][0], confs[key][1] or ''] for key in confs.keys()]
    echo.table(data)

    echo.print_sep(80)


@confcli.command()
@click.argument('key')
@click.argument('path')
@click.argument('desc', required=False)
def save(key, path, desc):
    """
    Save an existing config file to template folder.

    Similar to `add` command, but this command will just copy an existing config file to the template folder.

    key : str
        Shortcut for the config file.

    path : str
        Full path of the config file.

    desc : str
        Description of the config file.
    """
    _set_template(key, path, desc, edit=False)
    echo.done()
