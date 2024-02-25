try:
    import pytest
except ImportError:
    import unittest

from utils.strutil import print_length


def test_print_length_chinese_chars_should_count_as_2():
    assert print_length('中文') == 4
    assert print_length('中文word') == 8
