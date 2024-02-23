try:
    import pytest
except ImportError:
    import unittest

from utils.echoutils import echo


def test_call_echo_should_print_given_message(capfd):
    echo('test')
    out = capfd.readouterr().out
    assert echo.prefix + ' test' in out


def test_echo_done_should_print_Done(capfd):
    echo.done()
    out = capfd.readouterr().out

    assert 'Done!' in out


def test_get_prefix_right():

    assert echo._get_prefix() == '>> '
    assert echo._get_prefix(show_prefix=False) == ''
    assert echo._get_prefix('ppp') == 'ppp '

    echo.show_prefix = False
    assert echo._get_prefix(show_prefix=True) == '>> '


def test_wrong_fg_color_name_should_raise_value_error():
    with pytest.raises(TypeError) as e:
        echo('test', fg='reda')
    assert e.type == TypeError
    assert e.match('reda')


def test_right_color_name_should_pass(capfd):
    echo('test', fg='blue')
    assert 'test' in capfd.readouterr().out


def test_wrong_bg_color_name_should_raise_value_error():

    with pytest.raises(TypeError) as e:
        echo('test', bg='reda')

    assert e.type == TypeError
    assert e.match('reda')


def test_echo_separator_with_given_length(capfd):
    echo.print_sep()
    out = capfd.readouterr().out

    assert out == '=' * echo.sep_length + '\n'

    echo.print_sep(20, '*')
    out = capfd.readouterr().out

    assert out == '*' * 20 + '\n'


def test_echo_title(capfd):
    echo.print_title()
    out = capfd.readouterr().out

    assert echo.title in out
    assert echo.sep_char in out


def test_echo_with_out_new_line():
    echo('test', nl=False)
    echo('test', nl=False)
    echo('test', underline=True)
