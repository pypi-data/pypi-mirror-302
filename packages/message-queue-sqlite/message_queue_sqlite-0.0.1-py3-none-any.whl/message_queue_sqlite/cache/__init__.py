#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024-10-16 21:33:41
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   Cache 缓存
'''

import threading


class Cache:
    cache = {}
    lock = threading.Lock()
    
    @classmethod
    def set(cls, key, value: dict):
        with cls.lock:
            cls.cache[key] = value

    @classmethod
    def get(cls, key) -> dict:
        with cls.lock:
            return cls.cache.get(key)

    @classmethod
    def delete(cls, key):
        with cls.lock:
            del cls.cache[key]
        