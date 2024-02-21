import pytest
import os

from nescli.core.headers import PythonFileHeader
from nescli.core.headers.base import BaseFileHeader
from nescli.core.config import CLIConfig


@pytest.fixture(scope='module')
def config():
    return CLIConfig('./.test_config')


@pytest.fixture(scope='module', autouse=True)
def setup_config(config):
    config.set('user', 'root')
    config.set('mail', 'test@example.com')
    yield
    os.remove('./.test_config')


@pytest.fixture
def path():
    return os.path.join(os.path.dirname(__file__), __file__)


def test_base_file_header_should_raise_exception(path):
    with pytest.raises(NotImplementedError) as err:
        BaseFileHeader.generate(path)

    assert err.type == NotImplementedError


def test_python_file_header(config, path):
    pyheader = PythonFileHeader(config)
    header = pyheader.generate(path)

    assert type(header) == list
    assert len(list(filter(lambda x: 'root' in x, header))) == 1
    assert len(list(filter(lambda x: 'test@example.com' in x, header))) == 1
