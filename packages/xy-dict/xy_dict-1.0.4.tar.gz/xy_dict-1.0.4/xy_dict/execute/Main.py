# -*- coding: UTF-8 -*-
__author__ = 'helios'
__doc__ = 'Main'
'''
  * @File    :   Main.py
  * @Time    :   2023/06/03 10:29:37
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
'''
from xy_dict.Dict import Dict

def main():
    if callable(Dict):
        executor = Dict()
        if executor and hasattr(executor, "main") and callable(getattr(executor, "main")):
            main_func = getattr(executor, "main")
            try:
                main_func()
            except Exception:
                print("main函数运行错误")

if __name__ == "__main__":
    main()