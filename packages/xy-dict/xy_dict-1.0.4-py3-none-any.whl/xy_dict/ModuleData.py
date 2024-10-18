# -*- coding: UTF-8 -*-
__author__ = 'helios'
__doc__ = 'ModuleData'
'''
  * @File    :   ModuleData.py
  * @Time    :   2023/06/03 10:36:13
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
'''

from importlib_resources import files
import xy_dict

class ModuleData():
    
    def __init__(self):
        self.data_path = files(xy_dict.__name__).joinpath("data")
        