# -*- coding: UTF-8 -*-
__author__ = 'helios'
__doc__ = 'utils'
'''
  * @File    :   utils.py
  * @Time    :   2023/06/03 13:52:32
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
'''
from xy_string.utils import is_empty_string


def is_empty_dict(object_map: dict | None) -> bool:
    if object_map and isinstance(object_map, dict) and len(object_map.keys()) > 0:
        return False
    return True


def dict_get(
    object_map: dict | None,
    key: str | None,
    default=None,
):
    if not is_empty_dict(object_map) and not is_empty_string(key):
        return object_map.get(str(key)) if isinstance(object_map, dict) else default
    return default
