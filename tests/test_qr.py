try:
    import pytest
except ImportError:
    import unittest

import os
import shutil
import qrcode
from click.testing import CliRunner
import requests
import cv2

from nescli.commands.qrconsole import (
    qrconsole,
    _create_temp_folder,
    _remove_temp_folder,
    _temp_folder
)


@pytest.fixture
def temp_name():
    return 'test_nescli'


def test_temp_folder_should_be_delete_even_not_empty(temp_name):
    _create_temp_folder(temp_name)

    tmp_path = os.path.join(os.environ['TMPDIR'], temp_name)
    fn = os.path.join(tmp_path, 'temp.txt')

    with open(fn, 'w') as f:
        f.write('some text')

    assert os.path.exists(fn)

    _remove_temp_folder(tmp_path)

    assert not os.path.exists(tmp_path)


def test_create_temp_folder():
    _create_temp_folder()
    assert os.path.exists(_temp_folder())


def test_remove_temp_folder():
    _remove_temp_folder()
    assert not os.path.exists(_temp_folder())


@pytest.fixture
def qrobj() -> qrcode.QRCode:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )

    return qr


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.skip('Usage testing, irrelevant to the project.')
@pytest.mark.parametrize('url', [
    'https://gitee.com/miao123456miao/python-qrcode/raw/master/doc/module_drawers.png'
])
def test_parse_url_from_remote_image(qrobj, runner, tmp_path, url):

    result = runner.invoke(qrconsole, ['load', url])
    resp = requests.get(url)

    fn = os.path.join(tmp_path, os.path.basename(url))

    with open(fn, 'wb') as img:
        img.write(resp.content)

    reader = BarCodeReader()
    result = reader.decode(fn)

    os.remove(fn)

    # print(result[0])
    assert len(result) == 1
    assert result[0]['parsed'] == b'abcdefghijklmnopqrstuvwxyz'


@pytest.mark.skip('Usage testing, irrelevant to the project.')
def test_parse_qrcode(tmp_path, qrobj):
    qrobj.add_data('https://baidu.com/')
    img = qrobj.make_image()
    img.save('code.png')

    reader = BarCodeReader()
    result = reader.decode('code.png')

    print(str(result[0]['parsed'], encoding='utf-8'))


@pytest.mark.skip('Usage testing, irrelevant to the project.')
def test_parse_qrcode_with_cv2(qrobj):

    qrobj.add_data('https://baidu.com/')
    qrobj.make(fit=True)
    img = qrobj.make_image()
    img.save('code.png')

    qr_image = cv2.imread('code.png')
    qr_detector = cv2.QRCodeDetector()
    result, _, _ = qr_detector.detectAndDecode(qr_image)

    assert result == 'https://baidu.com/'
