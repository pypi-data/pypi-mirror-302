# -*- coding: UTF-8 -*-
__author__ = 'helios'
__doc__ = 'utils'
'''
  * @File    :   utils.py
  * @Time    :   2023/06/04 13:36:30
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
'''

import inspect

def count_of_function_arguments(func) -> int:
    """
    函数参数的数量

    Args:
        func (_type_): 函数

    Returns:
        int: 函数参数的数量
    """
    if inspect.isfunction(func):
        signature = inspect.signature(func)
        if signature:
            return len(signature.parameters)
    return 0

def validate_callable_func(func, args_count: int = 0) -> bool:
    """
    是否为可调用函数

    Args:
        func (_type_): 函数
        args_count (int, optional): 参数数量. Defaults to 0.

    Returns:
        bool: 是否为可调用函数
    """    
    count = count_of_function_arguments(func)
    return isinstance(args_count, int) and count >= args_count


def validate_callable_init_func(cls, args_count: int = 0) -> bool:
    """
    是否为可调用init函数

    Args:
        cls (_type_): 类
        args_count (int, optional): 参数数量. Defaults to 0.

    Returns:
        bool: 是否为可调用init函数
    """    
    count = 0
    if (
        "__init__" in dir(cls)
        and issubclass(cls, type)
        and inspect.isfunction(cls.__init__)
    ):
        count = count_of_function_arguments(cls.__init__)
    return isinstance(args_count, int) and count >= args_count


def has_func(obj, func_name: str, args_count: int = 0) -> bool:
    """
    某个对象是否拥有某函数

    Args:
        obj (Object): 对象
        func_name (str): 函数
        args_count (int, optional): 函数参数数量. Defaults to 0.

    Returns:
        bool: 某个对象是否拥有某函数
    """
    ok = False
    if hasattr(obj, func_name) and validate_callable_func(
        getattr(obj, func_name), args_count
    ):
        ok = True
    return ok


def empty_value(obj, a_type: type, default):
    """
    是否为空

    Args:
        obj (Object): 对象
        a_type (type): 对象类型
        default (Object): 默认对象

    Returns:
        _type_: 返回对象
    """
    if isinstance(obj, type(None)) and isinstance(default, type(None)):
        return None
    if isinstance(obj, type(None)):
        if not isinstance(default, a_type):
            return None
        else:
            return default
    return obj
