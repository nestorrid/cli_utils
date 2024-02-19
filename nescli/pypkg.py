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

KEY_ENV_USER = 'user'
KEY_ENV_MAIL = 'mail'
KEY_ENV_ADD_HEADER = 'add_header'
CONFIG_FILE = os.path.join(os.environ.get('HOME'), '.nespkg.conf')


def setup_project_basic_packages(ctx, param, value):

    if not value:
        return

    path = os.path.abspath('.')
    folder = path.rsplit('/', 1)[1]
    messages = []
    messages += _create_packages(path, folder)
    messages += _create_packages(path, 'tests')
    app = os.path.join(path, 'app.py')
    _create_file(app)
    messages.append(f'Create file: `app.py`.')

    for msg in messages:
        echo(msg)

    ctx.exit()


def show_config_info(ctx, param, value):
    if not value:
        return

    conf = _load_config()

    if conf:
        echo("PKG CONFIG INFO:", show_prefix=True)
        echo()
        for key, value in conf.items():
            echo(f'{key} : {value}')
    else:
        echo("Can't find config information.")
        echo("Use `--setuser` or `--setmail` to set user information first.")
    ctx.exit()


def echo(msg=None, fg='yellow', show_prefix=False, prefix='>>'):

    if not msg:
        click.echo(click.style('='*40, fg=fg))
        return

    if show_prefix:
        msg = prefix + " " + msg
    click.echo(click.style(msg, fg=fg))


def set_user(ctx, param, value):

    if not value:
        return

    _set_config(KEY_ENV_USER, value)
    echo(f'USERNAME is set to {value!r}')
    ctx.exit()


def set_mail(ctx, param, value):

    if not value:
        return

    _set_config(KEY_ENV_MAIL, value)
    echo(f'EMAIL is set to {value!r}')
    ctx.exit()


def _load_config():
    if os.path.exists(CONFIG_FILE):
        conf_obj = json.loads(Path(CONFIG_FILE).read_text())
        return conf_obj


def _set_config(key, value):
    conf_obj = _load_config() or {}
    conf_obj[key] = value
    with open(CONFIG_FILE, 'w') as f:
        f.write(json.dumps(conf_obj))


def set_show_header(ctx, param, value):

    conf = _load_config() or {}

    if not KEY_ENV_ADD_HEADER in conf:
        echo()
        echo('This is the first time you run `pkg`. Init file header is `ON`.')
        echo('If you don\'t want to add anything to the init file just run:\n    `pkg -H`\nto close it.')
        echo()
        _set_config(KEY_ENV_ADD_HEADER, value)
        return

    if conf[KEY_ENV_ADD_HEADER] == value:
        return

    _set_config(KEY_ENV_ADD_HEADER, value)
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

    messages = dict(
        new=[],
        turned=[],
        exists=[],
    )

    for name in names:
        path, pkg, target = _parse_package(name, is_path)
        if os.path.exists(target):
            if _check_is_package(target):
                msg = f'Package {pkg!r} is already exists. Nothing will be changed.'
                messages['exists'].append(msg)
            else:
                _convert_directory_to_package(target)
                msg = f'Folder {pkg!r} is already exists. Turned into package.'
                messages['turned'].append(msg)
        else:
            msg = _create_packages(path, pkg)
            messages['new'].extend(msg)

    _result_message(messages, verbose)


def _create_packages(path, pkg):

    messages = []

    if not os.path.exists(path):
        p, t = path.rsplit('/', 1)
        messages += _create_packages(p, t)

    target = os.path.join(path, pkg)
    os.mkdir(target)
    _convert_directory_to_package(target)
    messages.append(f'New package {pkg!r} is created.')

    return messages


def _result_message(messages, verbose):

    if verbose:
        for msg_list in messages.values():
            for msg in msg_list:
                click.echo(
                    click.style(msg, fg='green')
                )

    msg = f'Done! {len(messages["new"])!r} packages created.'
    if len(messages['turned']) > 0:
        msg += f" {len(messages['turned'])!r} directories turned into package."
    if len(messages['exists']) > 0:
        msg += f" {len(messages['exists'])!r} package is already exists."

    click.echo(
        click.style(msg, fg='yellow')
    )


def _init_file_header(path):

    conf = _load_config()
    if not conf[KEY_ENV_ADD_HEADER]:
        return []

    paths = path.rsplit('/', 2)

    header = [
        "# -*- coding: utf-8 -*-\n",
        f"# @File    :   {paths[1]}/{paths[2]}\n",
        f"# @Time    :   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
    ]
    if conf[KEY_ENV_USER]:
        header.append(f"# @Author  :   {conf[KEY_ENV_USER]}\n")
    if conf[KEY_ENV_MAIL]:
        header.append(f"# @Email   :   {conf[KEY_ENV_MAIL]}\n")

    header.append('\n""" docstring """')

    return header


def _convert_directory_to_package(target):

    name = os.path.join(target, '__init__.py')
    _create_file(name)


def _create_file(path):

    headers = _init_file_header(path)

    with open(path, 'w') as f:
        for line in headers:
            f.write(line)


def _check_is_package(target):
    path = os.path.join(target, '__init__.py')
    return os.path.exists(path)


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
