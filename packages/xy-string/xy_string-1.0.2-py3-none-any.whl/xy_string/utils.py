# -*- coding: UTF-8 -*-
__author__ = 'helios'
__doc__ = 'utils'
'''
  * @File    :   utils.py
  * @Time    :   2023/06/04 13:36:02
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
'''

from xy_type.utils import empty_value


def is_empty_string(a_string) -> bool:
    """
    是否为空字符串

    Args:
        a_string ( str):  字符串

    Returns:
        bool: 是否为空字符串
    """
    return not isinstance(a_string, str) or len(a_string) <= 0 or not a_string


def empty_string(a_string, default) -> str | None:
    """
    过滤空字符串

    Args:
        a_string (str):  字符串
        default (str):  默认

    Returns:
        str | None: 返回字符串
    """
    if is_empty_string(a_string=a_string) and is_empty_string(default):
        return None
    return empty_value(a_string, str, default)


import re


def contains_zh(a_string) -> bool:
    """
    是否含有中文

    Args:
        a_string (str): 字符串

    Returns:
        bool: 是否含有中文
    """
    if is_empty_string(a_string):
        return False
    zh_pattern = re.compile("[\u4e00-\u9fa5]+")
    match = zh_pattern.search(str(a_string))
    if match:
        return True
    return False
