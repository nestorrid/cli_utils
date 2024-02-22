# -*- coding: utf-8 -*-
# @File    :   message
# @Time    :   2024-02-20 15:57:13
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" Output message handler """

from functools import reduce
from typing import List, Tuple, Union, Literal, Iterable, Dict
from enum import Enum

from .click_util import echo


class MessageType(Enum):

    INFO = 'INFO'
    ERROR = 'ERROR'
    CREATE = 'CREATE'
    EXISTS = 'EXISTS'
    UPDATE = 'UPDATE'

    def __str__(self):
        return self.value


class Message:
    """
    .. _utils-Message:

    Message management utilities.
    """

    def __init__(self):
        self._msg: Dict[str, List] = dict()
        self._summary = dict()

    def push(
            self, msg: Union[Iterable[str], str], /,
            msg_type: Union[MessageType, str] = MessageType.INFO,
            show_type=False,
            prefix='>> ', show_prefix=False,
    ):
        if not self._msg.get(msg_type, None):
            self._msg[msg_type] = list()

        if isinstance(msg, str):
            msg = f'[{msg_type}] ' if show_type else "" + msg
            msg = prefix if show_prefix else "" + msg
            self._msg[msg_type].append(msg)
            return

        for m in msg:
            self.push(m, msg_type, show_type, prefix, show_prefix)

    def pop(self, msg_type: Union[MessageType, str] = MessageType.INFO) -> str | None:
        msg_list = self._msg.get(msg_type, None)
        if msg_list and len(msg_list) > 0:
            return msg_list.pop()

    def count(self, msg_type=None):
        if msg_type:
            return len(self._msg.get(msg_type, []))

        return reduce(
            lambda x, y: x + len(y),
            self._msg.values(), 0)

    def list(self, msg_type=MessageType.INFO):
        return self._msg.get(msg_type, [])

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value: Tuple[Union[MessageType, str], str]):
        self._summary[value[0]] = value[1]

    def echo(self, types=('all',), /, verbose=False):

        keys = self._msg.keys() if types == ('all', ) else types

        if verbose:
            self._echo_list(keys)
        else:
            for key in self._msg.keys():
                self._echo_summary(key)

    def _echo_summary(self, key):
        summary = self.summary.get(
            key, f"{key} message")
        echo(f'{summary}: {len(self._msg.get(key, []))}.')

    def _echo_list(self, keys):
        for key in keys:
            msg_list = self._msg.get(key, [])
            for msg in msg_list:
                echo(msg)

    def clear(self, types=('all',)):
        if types == ('all',):
            self._msg.clear()
            return

        for t in types:
            self._msg[t].clear()


msgbox = Message()
