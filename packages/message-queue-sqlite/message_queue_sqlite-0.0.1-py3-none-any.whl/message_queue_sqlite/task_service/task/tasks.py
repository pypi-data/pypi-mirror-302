#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tasks.py
@Time    :   2024-10-16 21:27:58
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   task functions
'''

import logging
from .task_base import TaskBase


class Tasks:
    tasks_functions = {}
    @classmethod
    def register(cls, task_name, task):
        cls.tasks_functions[task_name] = task

    @classmethod
    def get_task_function(cls, task_name) -> TaskBase:
        return cls.tasks_functions.get(task_name, None)
    
    @classmethod
    def get_all_task_names(cls):
        tasks_list = [task_name for task_name in cls.tasks_functions.keys()]
        logging.info(f"All tasks: {tasks_list}")
        return tasks_list
    