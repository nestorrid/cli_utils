import pytest

from utils import msgbox, MessageType as mt


@pytest.fixture(scope='module', autouse=True)
def init_msg():
    msgbox.push('some message')
    msgbox.push('some other message')
    msgbox.push('create message', msg_type=mt.CREATE)
    msgbox.push('custom type message', msg_type='custom', show_type=True)


def test_push_multiple_messages():
    msgbox.push([
        "message 1",
        "message 2"
    ])

    assert msgbox.count(mt.INFO) == 4


def test_message_count():
    assert msgbox.count() == 4
    assert msgbox.count(mt.CREATE) == 1
    assert msgbox.count(mt.INFO) == 2
    assert msgbox.count('custom') == 1


def test_get_unset_msg_list_should_get_empty_list():
    assert msgbox.list(mt.ERROR) == []


def test_echo_message_for_custom_type(capfd):
    msgbox.echo('test echo')


def test_set_message_summary():
    msgbox.summary = mt.CREATE, 'Craete something'
    print(msgbox.summary)


def test_echo_summary_should_contains_type_and_count(capfd):
    msgbox._echo_summary(mt.INFO)
    result = capfd.readouterr()

    assert mt.INFO.value in result.out
    assert str(msgbox.count(mt.INFO)) in result.out


def test_echo_summary_should_contain_specified_summary(capfd):
    msgbox.summary = mt.INFO, "test info"
    msgbox._echo_summary(mt.INFO)
    result = capfd.readouterr()

    assert "test info" in result.out
    assert str(msgbox.count(mt.INFO)) in result.out


def test_pop_message_should_get_last_message():
    _msg = msgbox.pop()
    assert _msg == 'some other message'
    assert msgbox.count(mt.INFO) == 1


def test_echo_list(capfd):
    msgbox._echo_list([mt.INFO, mt.ERROR])
    result = capfd.readouterr()
    assert 'some message' in result.out
    assert 'some other message' in result.out


def test_echo_all(capfd):
    msgbox.summary = 'custom', 'balabala'
    msgbox.echo('title')
    result = capfd.readouterr()

    assert 'title' in result.out
    assert '===' in result.out
    assert 'balabala: 1' in result.out


def test_list_message():
    assert len(msgbox.list()) == 2
