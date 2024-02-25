try:
    import pytest
except ImportError:
    import unittest

from utils import strutil as sutil


def test_str_width_limit():
    result = sutil.str_to_lines('这是一段目标文字, this is a test text', line_width=6)

    assert result[0] == '这是一'
    assert result[1] == '段目标'

    for s in result:
        assert sutil.print_length(s) <= 6
