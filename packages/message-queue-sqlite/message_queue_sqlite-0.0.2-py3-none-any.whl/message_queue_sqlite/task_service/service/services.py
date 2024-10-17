#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   services.py
@Time    :   2024-10-16 21:28:40
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   service functions
'''

import sqlite3
import logging
import uuid
import json
from typing import Callable
import threading
import time

from ...cache import Cache

class Services:
    services_callbacks = {}
    lock = threading.Lock()

    @classmethod
    def register_function(cls, task_id, function: Callable):
        cls.services_callbacks[task_id] = function

    @classmethod
    def run_callback(cls, task_id, result, middleware_path="./message_queue.db"):
        callback = cls.services_callbacks.get(task_id, None)
        try:
            if callback:
                callback(result)    
                cls.update_task_status(task_id, 5, middleware_path)
                logging.info(f"Callback for task {task_id} executed successfully")
            else:
                cls.update_task_status(task_id, 4, middleware_path)
                logging.warning(f"No callback registered for task {task_id}")
        except Exception as e:
            cls.update_task_status(task_id, 4, middleware_path)
            logging.error(f"Error while running callback for task {task_id}: {e}")
        finally:
            try:
                del cls.services_callbacks[task_id]
            except KeyError:
                pass

    @classmethod
    def update_task_status(cls, task_id, status, middleware_path="./message_queue.db"):
        with cls.lock:
            conn = sqlite3.connect(middleware_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE
                    messages
                SET
                    status = ?
                WHERE
                    id =?
                """,
                (status, task_id)
            )
            conn.commit()
            conn.close()
    
    @classmethod
    def create_send_message(cls, middleware_path:str):
        def send_message(task_name:str, 
                         task_args: dict, 
                         callback: Callable = lambda x: None,
                         priority: int = 0,
                         use_cache: bool = False):
            time.sleep(0.012)
            task_id = str(uuid.uuid4())
            if use_cache:
                new_task_args = {}
                cache_args = {}
                for key, value in task_args.items():
                    try:
                        new_task_args[key] = f"|{key}|"
                        cache_args[f"|{key}|"] = value
                    except Exception as e:
                        logging.error(f"Error while caching task_args: {e}")
                Cache.set(task_id, cache_args)
                task_args = new_task_args
            message = {
                "task_name": task_name,
                "task_args": task_args
            }
            conn = sqlite3.connect(middleware_path)
            corsor = conn.cursor()
            corsor.execute(
                """
                INSERT INTO 
                    messages (id, content, priority)
                    VALUES (?,?,?)
                """,
                (task_id, json.dumps(message), priority)
            )
            conn.commit()
            conn.close()

            cls.register_function(task_id, callback)
        return send_message
    