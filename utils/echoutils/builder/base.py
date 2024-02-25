# -*- coding: utf-8 -*-
# @File    :   builder/base.py
# @Time    :   2024-02-25 11:50:50
# @Author  :   Nestor
# @Email   :   admin@nestor.me

""" docstring """


class EchoBuilder:

    def __init__(self, data):
        self.data = data

    def echo(self):
        raise NotImplementedError(
            'Subclass of BaseEchoBuilder should implement this method.')
