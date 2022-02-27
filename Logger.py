# -*- coding: utf-8 -*-
"""
Created on Sep 26 2021

@author: Mourad Souag
"""
from enum import Enum
class LogLevel(Enum):
    ALL =3
    FILE = 1
    DISPLAY = 2
    NONE = 0

class Logger():

    def __init__(self, level= LogLevel.NONE):
        self._level = LogLevel.NONE
        self.SetLevel(level)

    def SetLevel(self, level= LogLevel.NONE):
        assert level != LogLevel.ALL, "Log level not supported"
        assert level != LogLevel.FILE, "Log level not supported"
        self._level = level
         
    def log(self, text=""):
        if self._level == LogLevel.DISPLAY:
            print(text)
