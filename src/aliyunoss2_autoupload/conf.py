# -*- coding: utf-8 -*-

"""
Config file loader
"""

import logging.config
import os
from io import FileIO

import yaml

try:
    from yaml import CSafeLoader as YamlLoader
except ImportError:
    from yaml import SafeLoader as YamlLoader

from . import glb
from . import version

__all__ = ['load_program_config', 'load_logging_config']

DEFAULT_PROGRAM_CONFIG_PATH = 'conf/{0}.yml'.format(version.NAME)
ENVIRON_PROGRAM_CONFIG_PATH = '{0}_CONFIG'.format(version.NAME.upper())

DEFAULT_LOGGING_CONFIG_PATH = 'conf/{0}.log.yml'.format(version.NAME)
ENVIRON_LOGGING_CONFIG_PATH = '{0}_LOG_CONFIG'.format(version.NAME.upper())


def load_program_config():
    """加载配置文件

    :return: 配置字典
    :rtype: dict

    * 如果设置了环境变量 ``DEFAULT_PROGRAM_CONFIG_PATH`` ，以该环境变量的值作为配置文件路径。
    * 否则以相对路径 ``config/prog.yaml`` 作为配置文件路径。
    """
    file_path = os.environ.get(ENVIRON_PROGRAM_CONFIG_PATH)
    if not file_path:
        file_path = DEFAULT_PROGRAM_CONFIG_PATH
    glb.config = config = yaml.load(FileIO(file_path), YamlLoader)
    return config


def load_logging_config():
    """加载 logging 配置文件

    * 如果设置了环境变量 ``DEFAULT_LOGGING_CONFIG_PATH`` ，以该环境变量的值作为配置文件路径。
    * 否则以相对路径 ``config/log.yaml`` 作为配置文件路径。
    """
    file_path = os.environ.get(ENVIRON_LOGGING_CONFIG_PATH)
    if not file_path:
        file_path = DEFAULT_LOGGING_CONFIG_PATH
    try:
        config = yaml.load(FileIO(file_path), YamlLoader)
        logging.config.dictConfig(config)
    except Exception as err:
        logging.warning(
            'Load logging config file `%s` failed: %s', file_path, err)
        logging.basicConfig()
