# -*- coding: utf-8 -*-

"""
默认配置
当有config_override.py文件时，会覆盖当前文件的配置信息
"""

configs = {
    'debug': True,
    'db': {
        'host': '8.129.132.234',
        'port': 3306,
        'user': '13226',
        'password': 'qweqwe123',
        'db': 'awesome'
    },
    'session': {
        'secret': 'Awesome'
    }
}