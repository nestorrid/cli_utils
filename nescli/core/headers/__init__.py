__all__ = ['python_header']

from .pyheader import PythonFileHeader
from nescli.core.config import config


python_header = PythonFileHeader(config)
