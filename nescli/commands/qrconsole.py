# -*- coding: utf-8 -*-
# @File    :   commands/qrconsole.py
# @Time    :   2024-02-22 11:01:16
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" docstring """

import os
import shutil

import qrcode
import click
import requests
import cv2

from nescli import config
from utils.strutil import QRCode as QRCodeCharacter
from utils import echo


@click.group()
def qrconsole():
    """
    qrconsole is a tool to print qrcode under the command line environment. A 3*3 qrcode may like this:

    \b
    ██  ██
      ██
    ██  ██

    NOTE: To get this image in right format you need a `mono space` font, 
    and equivalent line height with the font size in your terminal.

    If you're using vscode, default settings will be good.
    """
    pass


@qrconsole.command()
@click.argument('key')
@click.argument('url')
def set(key, url):
    """
    Convert a given url to QR data, and cache with the given key.
    """
    old = config.get(key)
    if old:
        if old != url:
            if not echo.confirm(
                f'KEY: {key!r} is already set to: {old!r}.\n   Do you want to replace it with: {url!r}?'
            ):
                echo('Canceld.')
                return
        else:
            return

    config.set(key, url)
    echo(f'cached: {key}={url}.')


@qrconsole.command()
@click.argument('resource')
def load(resource):
    """
    Load resource from the given string.

    RESOURCE

        Path string or url to QRCode image. for example:

        \b
        * http://url/to/qrcode.png
        * /path/to/qrcode.png
    """
    path = resource
    if _is_url(resource):
        echo('Load image from URL: %s' % resource)
        _save_image_from_url(resource, 'tmp_img')
        path = os.path.join(_temp_folder(), 'tmp_img')

    if not os.path.exists(path):
        echo(f'Image {path!r} is not found.', fg=echo.color_red)
        return

    echo('parsing...')

    result = _parse_qrcode_image(path)

    if len(result) == 0:
        echo(
            'Failed for parsing resource: %s' %
            resource, fg=echo.color_red)
        return

    echo('Result for resource: %s' % resource)
    echo(result, fg=echo.color_cyan, prefix='   ', underline=True)
    _remove_temp_folder()


@qrconsole.command()
@click.argument('key')
def show(key):
    """
    Print QRCode in the terminal with the given key or url.

    KEY:
        Cached key with command `set` or url.
    """
    if _is_url(key):
        _print_ascii_qrcode(key)
        return

    url = config.get(key)
    echo(url)
    if url:
        _print_ascii_qrcode(url)
    else:
        echo(f'Can not find cached key {key!r}.', fg=echo.color_red)


def _parse_qrcode_image(path):
    img = cv2.imread(path)
    result, _, _, = cv2.QRCodeDetector().detectAndDecode(img)
    return result


def _create_temp_folder(name='nescli'):
    try:
        os.mkdir(_temp_folder(name))
    except FileExistsError:
        pass


def _temp_folder(name='nescli'):
    return os.path.join(os.environ['TMPDIR'], name)


def _remove_temp_folder(name='nescli'):
    try:
        shutil.rmtree(_temp_folder(name))
    except FileNotFoundError:
        pass


def _save_image_from_url(url: str, name: str):
    _create_temp_folder()
    fn = os.path.join(_temp_folder(), name)

    resp = requests.get(url)

    with open(fn, 'wb') as f:
        f.write(resp.content)


def _setup_qr() -> qrcode.QRCode:
    return qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2
    )


def _print_ascii_qrcode(url):
    qr = _setup_qr()
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii()
    return qr.get_matrix


def _is_url(arg: str):
    return arg.startswith('http://') or arg.startswith('https://')
