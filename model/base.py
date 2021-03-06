# coding:utf-8

import abc


class Base(metaclass=abc.ABCMeta):
    """Abstract object to enforce serialize presence"""

    @abc.abstractmethod
    def serialize(self):
        """turn the object into a dictionnary with argument
         name as key and argument value as value"""
        pass
