try:
    import pytest
except ImportError:
    import unittest

from pathlib import Path
import os
import json

from nescli.commands.conf_manage import (
    _check_conf_template_folder,
    _set_template,
    _remove_template,
    _get_template
)
from nescli import config


@pytest.fixture
def config_path():
    return os.path.join(os.environ['HOME'], '.nescli.conf')


def test_template_folder_should_exists():
    assert _check_conf_template_folder()


@pytest.mark.skip()
def test_set_new_template(config_path, tmp_path):
    tmp = os.path.basename(tmp_path)
    _set_template(tmp, tmp, 'desc')
    assert json.dumps({tmp: [tmp, 'desc']}) in Path(config_path).read_text()
    _remove_template(tmp)


def test_remove_template():
    _remove_template('a')
    assert _get_template('a') == None


@pytest.mark.skip()
def test_get_template(tmp_path):
    tmp = os.path.basename(tmp_path)
    _set_template(tmp, tmp, 'desc')
    result = _get_template(tmp)
    assert [tmp, 'desc'] == [result.name, result.desc]
    _remove_template(tmp)
