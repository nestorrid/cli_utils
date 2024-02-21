import pytest
import os

from nescli.core.config import CLIConfig


@pytest.fixture(scope='module')
def config():
    return CLIConfig('./.test_config')


@pytest.fixture(scope='module', autouse=True)
def preset_config(config):
    config.set('preset', True)
    yield
    os.remove('./.test_config')


def test_config_file_should_be_saved_after_set_new_value(config):
    config.set('test', 'aaa')
    assert os.path.exists(config._path)


def test_load_preset_will_be_True(config):
    assert config.get('preset')


def test_remove_config(config):
    config.remove('preset')
    assert config.get('preset') == None
