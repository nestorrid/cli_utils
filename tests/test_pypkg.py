import os

import pytest
from click.testing import CliRunner
import click
import shutil

from nescli.pypkg import pkg, _parse_package, _convert_directory_to_package


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_names(runner):
    result = runner.invoke(pkg, ['a', 'b'])
    runner
    assert result.exit_code == 0


def test_unpack_list():
    a, b = [1, 2]
    assert a == 1
    assert b == 2


@pytest.mark.parametrize("name", [
    'some',
    'package',
    'name',
])
def test_parse_package_name(name):
    pwd = os.path.abspath('.')
    path, pkg = _parse_package(name, absolute=False)
    assert pwd == path
    assert pkg == name


def test_parse_package_name_with_slash_will_raise_exception():
    with pytest.raises(click.BadParameter) as e:
        _parse_package('package/name', absolute=False)

    assert e.type == click.BadParameter


@pytest.mark.parametrize('name', [
    './path/to/package',
    './other/path/to/pack/age',
])
def test_parse_package_with_absolute_path(name):
    target = os.path.abspath(name.rsplit('/', 1)[0])
    path, pkg = _parse_package(name, absolute=True)

    assert path == target
    assert pkg == name.rsplit('/', 1)[1]


def test_convert_directory_to_package():
    path = os.path.abspath('./demo')
    if not os.path.exists(path):
        os.makedirs(path)

    _convert_directory_to_package(path)

    assert os.path.exists(os.path.join(path, '__init__.py'))

    shutil.rmtree(path)
