# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'Decorators'
'''
  * @File    :   Decorators.py
  * @Time    :   2024/03/21 19:59:55
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, 希洋 (Ship of Ocean)
  * @Desc    :   
'''


def singleton(cls):
    """ 装饰器函数
        实现方式:
            @singleton
            class Cls(object):
                def __init__(self):
                    pass

    Returns:
        _type_: 返回类型
    """
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner


class Singleton(object):
    """ 类装饰器
        实现方式:
            @Singleton
            class Cls(object):
                def __init__(self):
                    pass

    Args:
        object (_type_): 父类
    """

    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]
