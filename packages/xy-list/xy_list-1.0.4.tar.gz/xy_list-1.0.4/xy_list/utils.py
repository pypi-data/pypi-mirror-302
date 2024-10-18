# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "utils"
"""
  * @File    :   utils.py
  * @Time    :   2023/06/03 14:02:28
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, 希洋 (Ship of Ocean)
  * @Desc    :   None
"""


def is_empty_list(object_list: list | None) -> bool:
    if object_list and isinstance(object_list, list) and len(object_list) > 0:
        return False
    return True
