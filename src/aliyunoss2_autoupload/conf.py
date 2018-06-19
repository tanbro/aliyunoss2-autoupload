# -*- coding: utf-8 -*-

"""
Config file loader
"""

from __future__ import absolute_import, unicode_literals

import logging.config
import os
from io import FileIO

import yaml
from marshmallow import Schema, fields

from . import glb
from . import version

try:
    from yaml import CSafeLoader as YamlLoader
except ImportError:
    from yaml import SafeLoader as YamlLoader

__all__ = ['load_program_config', 'load_logging_config']

DEFAULT_PROGRAM_CONFIG_PATH = 'conf/{0}.yml'.format(version.NAME)
ENVIRON_PROGRAM_CONFIG_PATH = '{0}_CONF'.format(version.NAME.upper().replace('-', '_'))

DEFAULT_LOGGING_CONFIG_PATH = 'conf/{0}.log.yml'.format(version.NAME)
ENVIRON_LOGGING_CONFIG_PATH = '{0}_LOG_CONF'.format(version.NAME.upper().replace('-', '_'))


class OssSchema(Schema):
    """Aliyun OSS configuration schema"""

    name = fields.String(required=True)
    """Name of your Aliyun OSS bucket"""

    endpoint = fields.String(required=True)
    """Endpoint URL of Aliyun OSS bucket"""

    cname = fields.String(missing='')
    """cname of the domain of Aliyun OSS bucket. Empty if no cname."""

    access_key_id = fields.String(required=True)
    """Access Key ID of Aliyun OSS bucket"""

    access_key_secret = fields.String(required=True)
    """Access Key Secret of Aliyun OSS bucket"""


class DirSchema(Schema):
    """Directory name configuration schema"""

    rel_dir = fields.String(missing='')
    """Calculate uploading file relative name by this local directory"""

    oss_dir = fields.String(missing='')
    """Upload files to OSS in this dir"""

    bak_dir = fields.String(missing='')
    """Move uploaded file the the directory. It MUST be a different dir from where the files are. If not, the file will be uploaded again and again.
    """


class WatcherSchema(Schema):
    interval = fields.Integer(missing=30)
    """The time interval(seconds) this program scan the directory"""

    write_complete_time = fields.Integer(missing=30)
    """If the interval between the current time and the file\'s modification time is greater than this value, the write is considered complete.
    """

    patterns = fields.String(required=True)
    """Pattern of the files to watch and upload"""

    recursive = fields.Boolean(missing=False)
    """If find patterns recursively"""

    max_workers = fields.Integer(allow_none=True, missing=None)
    """pool of at most max_workers threads to execute upload/backup tasks. If max_workers is None or not given, it will default to the number of processors on the machine, multiplied by 5.
    """


class ConfSchema(Schema):
    oss = fields.Nested(OssSchema, required=True)
    dir = fields.Nested(DirSchema)
    watcher = fields.Nested(WatcherSchema, required=True)


conf_scheme = ConfSchema()


def load_program_config():
    """加载配置文件

    :return: 配置字典
    :rtype: dict

    * 如果设置了环境变量 ``ALIYUNOSS2_AUTOUPLOAD_CONF`` ，以该环境变量的值作为配置文件路径。
    * 否则以相对路径 ``conf/aliyunoss2-autoupload.yml`` 作为配置文件路径。
    """
    # load
    file_path = os.environ.get(ENVIRON_PROGRAM_CONFIG_PATH)
    if not file_path:
        file_path = DEFAULT_PROGRAM_CONFIG_PATH
    with open(file_path) as f:
        data = yaml.load(f, YamlLoader)
    # validate!
    config = conf_scheme.load(data)  # type: dict
    glb.config = config
    return config


def load_logging_config():
    """加载 logging 配置文件

    * 如果设置了环境变量 ``ALIYUNOSS2_AUTOUPLOAD_LOG_CONF`` ，以该环境变量的值作为配置文件路径。
    * 否则以相对路径 ``conf/aliyunoss2-autoupload.log.yml`` 作为配置文件路径。
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
