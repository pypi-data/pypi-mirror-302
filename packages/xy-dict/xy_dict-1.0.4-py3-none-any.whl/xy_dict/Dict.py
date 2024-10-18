# -*- coding: UTF-8 -*-
__author__ = 'helios'
__doc__ = 'Module'
'''
  * @File    :   Module.py
  * @Time    :   2023/06/03 10:29:52
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
'''
from .utils import is_empty_dict
from xy_list.utils import is_empty_list


class Dict:
    current_depth = 0
    current_repeat_count = 0
    current_map = {}
    object_map = {}
    key_map = {}
    current_key = None
    current_value = None
    depth = -1
    repeat_count = -1

    def __init__(self, object_map: dict):
        self.object_map = object_map

    def reset(self):
        self.current_depth = 0
        self.current_repeat_count = 0
        self.current_map = self.object_map
        self.key_map = {}
        self.current_key = None
        self.depth = -1
        self.repeat_count = -1

    def search_k(self, key, depth=-1, repeat_count=-1):
        self.reset()
        self.current_key = key
        self.depth = depth
        self.repeat_count = repeat_count
        self.key_map = self.__search_k(self.object_map)

    def search_v(self, value, depth=-1, repeat_count=-1):
        self.reset()
        self.current_value = value
        self.depth = depth
        self.repeat_count = repeat_count
        self.key_map = self.__search_v(self.object_map)

    def search_kv(self, key, value, depth=-1, repeat_count=-1):
        self.reset()
        self.current_key = key
        self.current_value = value
        self.depth = depth
        self.repeat_count = repeat_count
        self.key_map = self.__search_kv(self.object_map)

    def add_depth(self) -> bool:
        self.current_depth += 1
        return self.validate()

    def add_repeat(self) -> bool:
        self.current_repeat_count += 1
        return self.validate()

    def validate(self):
        unvalidate = (self.depth > 0 and self.current_depth >= self.depth) or (
            self.repeat_count > 0 and self.current_repeat_count >= self.repeat_count
        )
        return unvalidate is False

    def __search_k(self, object_map: dict, add_depth=True):
        key_map = {}
        if not self.validate():
            return key_map
        if not is_empty_dict(
            object_map=object_map,
        ):
            if add_depth is True:
                self.add_depth()
            if not self.validate():
                return key_map
            for key, value in object_map.items():
                if not self.validate():
                    break
                if key == self.current_key:
                    self.add_repeat()
                    key_map.setdefault(
                        key,
                        value,
                    )
                    if not is_empty_dict(
                        value,
                    ) and isinstance(
                        value,
                        dict,
                    ):
                        sub_key_map = {}
                        for sub_key, sub_value in value.items():
                            if not is_empty_dict(
                                sub_value,
                            ):
                                key_map_result = self.__search_k(
                                    sub_value,
                                    add_depth=False,
                                )
                                if not is_empty_dict(
                                    key_map_result,
                                ):
                                    sub_key_map.update(
                                        {
                                            sub_key: key_map_result,
                                        },
                                    )
                                    if not self.validate():
                                        break
                        if not is_empty_dict(
                            sub_key_map,
                        ):
                            if add_depth is False:
                                self.add_depth()
                            key_map.update(
                                {
                                    key: sub_key_map,
                                },
                            )
                    if not is_empty_list(value) and isinstance(value, list):
                        sub_list = []
                        for sub_value in value:
                            if not is_empty_dict(sub_value):
                                sub_key_map = self.__search_k(
                                    sub_value,
                                    add_depth=False,
                                )
                                if not is_empty_dict(sub_key_map):
                                    sub_list.append(sub_key_map)
                                    if not self.validate():
                                        break
                        if not is_empty_list(sub_list):
                            if add_depth is False:
                                self.add_depth()
                            key_map.update(
                                {
                                    key: sub_list,
                                },
                            )
                else:
                    if not is_empty_dict(value) and isinstance(
                        value,
                        dict,
                    ):
                        map_result = self.__search_k(
                            value,
                            add_depth=False,
                        )
                        if not is_empty_dict(map_result):
                            if add_depth is False:
                                self.add_depth()
                            key_map.setdefault(key, map_result)
                    if not is_empty_list(value) and isinstance(value, list):
                        sub_list = []
                        for sub_value in value:
                            if not is_empty_dict(sub_value):
                                sub_key_map = self.__search_k(
                                    sub_value,
                                    add_depth=False,
                                )
                                if not is_empty_dict(sub_key_map):
                                    sub_list.append(sub_key_map)
                                    if not self.validate():
                                        break
                        if not is_empty_list(sub_list):
                            if add_depth is False:
                                self.add_depth()
                            key_map.update(
                                {
                                    key: sub_list,
                                },
                            )
                if not self.validate():
                    break
        return key_map

    def __search_kv(self, object_map: dict, add_depth=True):
        key_map = {}
        if not self.validate():
            return key_map
        if not is_empty_dict(
            object_map=object_map,
        ):
            if add_depth is True:
                self.add_depth()
            if not self.validate():
                return key_map
            for key, value in object_map.items():
                if not self.validate():
                    break
                if key == self.current_key and value == self.current_value:
                    self.add_repeat()
                    key_map.setdefault(
                        key,
                        value,
                    )
                else:
                    if not is_empty_dict(value) and isinstance(
                        value,
                        dict,
                    ):
                        map_result = self.__search_kv(
                            value,
                            add_depth=False,
                        )
                        if not is_empty_dict(map_result):
                            if add_depth is False:
                                self.add_depth()
                            key_map.setdefault(key, map_result)
                    if not is_empty_list(value) and isinstance(value, list):
                        sub_list = []
                        for sub_value in value:
                            if not is_empty_dict(sub_value):
                                sub_key_map = self.__search_kv(
                                    sub_value,
                                    add_depth=False,
                                )
                                if not is_empty_dict(sub_key_map):
                                    sub_list.append(sub_key_map)
                                    if not self.validate():
                                        break
                        if not is_empty_list(sub_list):
                            if add_depth is False:
                                self.add_depth()
                            key_map.update(
                                {
                                    key: sub_list,
                                },
                            )
                if not self.validate():
                    break
        return key_map

    def __search_v(self, object_map: dict, add_depth=True):
        key_map = {}
        if not self.validate():
            return key_map
        if not is_empty_dict(
            object_map=object_map,
        ):
            if add_depth is True:
                self.add_depth()
            if not self.validate():
                return key_map
            for key, value in object_map.items():
                if not self.validate():
                    break
                if value == self.current_value:
                    self.add_repeat()
                    key_map.setdefault(
                        key,
                        value,
                    )
                else:
                    if not is_empty_dict(value) and isinstance(
                        value,
                        dict,
                    ):
                        map_result = self.__search_v(
                            value,
                            add_depth=False,
                        )
                        if not is_empty_dict(map_result):
                            if add_depth is False:
                                self.add_depth()
                            key_map.setdefault(key, map_result)
                    if not is_empty_list(value) and isinstance(value, list):
                        sub_list = []
                        for sub_value in value:
                            if sub_value == self.current_value:
                                sub_list.append(sub_value)
                                break
                            if not is_empty_dict(sub_value):
                                sub_key_map = self.__search_v(
                                    sub_value,
                                    add_depth=False,
                                )
                                if not is_empty_dict(sub_key_map):
                                    sub_list.append(sub_key_map)
                                    if not self.validate():
                                        break
                        if not is_empty_list(sub_list):
                            if add_depth is False:
                                self.add_depth()
                            key_map.update(
                                {
                                    key: sub_list,
                                },
                            )
                if not self.validate():
                    break
        return key_map


# import json

# json_file_path = "/home/helios/workspace/beachstudio/business/tb101_cloudphone/development/tb101_cp_server/tb101_cp_server/assets/cloud_mobile_urls.json"


# def content():
#     with open(json_file_path, "r", encoding="utf-8") as json_file:
#         return json.load(json_file)


# d = Dict(content())
# d.search_kv("name", 'GPS定位设置', depth=10, repeat_count=-1)
