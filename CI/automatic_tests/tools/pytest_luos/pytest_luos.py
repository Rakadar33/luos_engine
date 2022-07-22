# -*- coding: utf-8 -*-
from functools import wraps
from tools.pytest_luos.hub_controller import *
from tools.pytest_luos.luos_controller import *
from tools.pytest_luos.mcu_controller import *
from tools.pytest_luos.test_engine import *

def singleton(orig_cls):
    orig_new = orig_cls.__new__
    instance = None

    @wraps(orig_cls.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = orig_new(cls)
        return instance
    orig_cls.__new__ = __new__
    return orig_cls

@singleton
class LuosPytest:
    def __init__(self):
        self.engine= Engine()
        self.luos= LuosControl()
        self.mcu= McuControl()
        self.basic_hub= HubControl("default")
        self.prog_hub= HubControl("capable_robot")

    def init_platform(self):
        from tools.pytest_luos.config.platform import get_platform
        self.luos.platform= get_platform()
        self.mcu.platform= get_platform()
