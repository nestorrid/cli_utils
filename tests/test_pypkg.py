import os

import pytest
from click.testing import CliRunner
import click
import shutil

from nescli.commands.pypkg import pkg, _parse_package, _convert_directory_to_package


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.mark.parametrize('names', [
    ['a', 'b'],
    ['aa/aa', 'bb/bb']
])
def test_names(runner, names, tmp_path):
    args = ['-p', tmp_path] + names
    result = runner.invoke(pkg, args)
    assert result.exit_code == 0

    # path = os.path.abspath('.')
    for name in names:
        temp = os.path.join(tmp_path, name)
        assert os.path.exists(temp)
        shutil.rmtree(temp)


@pytest.mark.parametrize("name", [
    'some',
    'package',
    'name',
])
def test_parse_package_name(name):
    pwd = os.path.abspath('.')
    folder, pkg, path = _parse_package(name)
    assert pwd == folder
    assert pkg == name
    assert path == os.path.join(pwd, name)


def test_convert_directory_to_package():
    path = os.path.abspath('./demo')
    if not os.path.exists(path):
        os.makedirs(path)

    _convert_directory_to_package(path)

    assert os.path.exists(os.path.join(path, '__init__.py'))

    shutil.rmtree(path)
