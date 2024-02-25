try:
    import pytest
except ImportError:
    import unittest

from functools import reduce

from utils.echoutils import echo
from utils import strutil as sutil


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


def test_echo_statments(capfd):
    from utils import es
    echo.statments(
        'asdf',
        es('aaaa').red.bold,
        'bbb',
        es('ccc').red.bold,
    )

    assert '>> asdfaaaabbbccc\n' in capfd.readouterr().out


@pytest.fixture()
def lines() -> list:
    lines = [
        ['name', 'age', 'score'],
        ['jack', '18', '120'],
        ['john', '18', '120'],
        ['marry', '18', '120'],
        ['tom', '18', '120'],
        ['刘三儿', '18', '120'],
    ]
    return lines


def test_echo_table(lines):
    echo.table(lines)


def test_echo_table_with_different_columns_should_raise_value_error(lines):
    lines.append([
        '1', '2', '3', '4'
    ])

    with pytest.raises(ValueError) as e:
        echo.table(lines)

    assert e.type == ValueError


def test_echo_table_header(lines, capfd):
    echo.table(lines)
    outlines = [
        '┌───────┬────┬──────┐',
        '│name   │age │score │',
        '├───────┼────┼──────┤',
        '│jack   │18  │120   │',
        '│john   │18  │120   │',
        '│marry  │18  │120   │',
        '│tom    │18  │120   │',
        '│刘三儿 │18  │120   │',
        '└───────┴────┴──────┘',
    ]
    out = capfd.readouterr().out
    for line in outlines:
        assert line in out


def test_adjust_col_width():
    widths = echo._adjust_column_width(
        [5, 8, 10, 40, 40]
    )
    print(widths)
    assert reduce(lambda x, y: x + y, widths) <= echo.max_length


def test_adjust_line_width():
    widths = echo._adjust_column_width(
        [6, 8, 10, 40, 40]
    )
    line = [
        'asdf',
        '中文字符串',
        'asdfasdf',
        'test ' * 15,
        'test ' * 20,
    ]

    result = echo._adjust_line_width(line, widths)
    assert len(result) == 4
    assert 'asdf' in result[0]
    assert '中文字' in result[0]
