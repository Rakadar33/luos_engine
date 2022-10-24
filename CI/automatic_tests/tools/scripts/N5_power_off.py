# coding:utf-8
from tools.pytest_luos.config.platform import create_platform

platform= create_platform()
platform.init_platform()
platform.basic_hub.disable(5)

