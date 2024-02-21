try:
    import pytest
except ImportError:
    import unittest

import os
from nescli.commands.file import _find_tests_directory


def test_no_args_should_find_project_tests_folder():
    path = os.path.dirname(os.path.abspath(__file__))
    test_folder = _find_tests_directory()
    assert path == test_folder


def test_nested_path_should_find_project_tests_folder():
    path = os.path.dirname(os.path.abspath(__file__))
    test_folder = _find_tests_directory(os.path.join(path, 'aaa/bbb/ccc'))
    assert path == test_folder


def test_no_tests_path_should_return_none():
    path = _find_tests_directory("/aaa/bbb/ccc")
    assert path == None
