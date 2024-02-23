try:
    import pytest
except ImportError:
    import unittest

from utils import es, echo


def test_create_stat_with_single_msg(capfd):
    print(es('aaa'))
    assert 'aaa' in capfd.readouterr().out


def test_echo_statment_add_int_should_raise_type_error():
    with pytest.raises(TypeError) as e:
        es('aaa') + 1

    assert e.type == TypeError


def test_echo_multiple_statment_should_print_in_single_line(capfd):
    stmt = es('aaa').add('bbb').add(es('ccc')).end(with_prefix='>>')

    assert '>> aaabbbccc\n' == capfd.readouterr().out


def test_echo_multiple_statments_with_styles(capfd):
    es('test ').cyan.bold.add(
        es('stmt').magenta.underline.add(' ')
    ).add(
        es('text').white.red_bg
    ).end(with_prefix='>>')

    assert '>> test stmt text\n' == capfd.readouterr().out
