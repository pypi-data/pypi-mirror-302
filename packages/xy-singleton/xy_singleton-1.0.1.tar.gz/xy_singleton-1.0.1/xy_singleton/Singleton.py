# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'Singleton'
'''
  * @File    :   Singleton.py
  * @Time    :   2024/03/21 20:00:08
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, 希洋 (Ship of Ocean)
  * @Desc    :   
'''

class CallSingleton(type):
    """使用元类中的 __call__() 方法实现
        实现方式:
            class Foo(metaclass=CallSingleton):
                pass

    Args:
        type (_type_): 父类
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class NewSingleton(object):
    """使用 __new__() 方法实现
        实现方式:
            class Foo(Singleton):
                pass

    Args:
        object (_type_): 父类
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass
