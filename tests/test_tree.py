import os

import pytest
from click.testing import CliRunner

from nescli.tree import tree


@pytest.fixture
def runner():
    return CliRunner()


def test_default_targt_should_be_current_directory(runner):
    result = runner.invoke(tree, ['-t', '.'])
    assert result.exit_code == 0
    assert 'nescli' in result.output


def test_tree_file_should_raise_error(runner):
    filepath = os.path.join(os.path.abspath('.'), __file__)
    result = runner.invoke(
        tree, ['-t', filepath])


def test_list_filter():
    contents = ['...', '123', '.asdf']
    result = list(filter(lambda x: not x.startswith('.'), contents))
    assert len(result) == 1
