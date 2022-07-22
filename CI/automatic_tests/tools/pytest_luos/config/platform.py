# -*- coding: utf-8 -*-
from tools.pytest_luos.pytest_luos import LuosPytest

def create_platform():
    return LuosPytest()

def get_platform():
    return create_platform()