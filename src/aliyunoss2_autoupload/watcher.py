#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, with_statement, print_function

import os
import sys
from glob import iglob
from time import time
from threading import Lock
from multiprocessing.pool import ThreadPool
from shutil import move

import oss2
from oss2.exceptions import OssError

from . import glb
from .utils.loggermixin import LoggerMixin

try:
    import crcmod._crcfunext
except ImportError as err:
    _crc = False
    print('{0}. CRC will be DISABLED'.format(err), file=sys.stderr)
else:
    _crc = True


__all__ = ['Watcher']


class Watcher(LoggerMixin):

    _files = {}  # type: Dict[str, type(None)]
    _file_lock = Lock()  # type: threading.Lock
    _pool = None  # type: multiprocessing.Pool
    _bucket = None  # type: oss2.Bucket

    @classmethod
    def initialize(cls):
        if not _crc:
            cls.get_logger().warning('CRC for oss2 is disabled')

        cls._pool = ThreadPool()

        cfg = glb.config['oss']
        auth = oss2.Auth(cfg['access_key_id'], cfg['access_key_secret'])
        is_cname = bool(cfg['cname'])
        cls._bucket = oss2.Bucket(
            auth, cfg['endpoint'], cfg['name'], is_cname=is_cname, enable_crc=_crc
        )

    @classmethod
    def finalize(cls):
        pass

    @classmethod
    def scan_once(cls):  # type: (cls, str)->None
        logger = cls.get_logger()
        logger.debug('scan_once() >>>')
        now_ts = time()

        for path in iglob(glb.config['watcher']['patterns'], recursive=bool(glb.config['watcher']['recursive'])):
            logger.debug('scan_once(): file: %s', path)
            with cls._file_lock:
                if path not in cls._files:
                    # is file write completed? (According to last modify time)
                    mod_ts = os.path.getmtime(path)
                    if now_ts - mod_ts > glb.config['watcher']['write_complete_time']:
                        cls.get_logger().info('scan_once(): file write completed: %s', path)
                        cls._files[path] = None
                        cls._pool.apply_async(cls.upload_one, (path, ))

        logger.debug('scan_once() <<<')

    @classmethod
    def upload_one(cls, path):  # type: (cls, str)->None
        logger = cls.get_logger()
        try:
            logger.debug('upload_one(path=%s) >>>', path)
            rel_dir = glb.config['dir']['rel_dir']
            if rel_dir:
                rel_path = os.path.relpath(path, rel_dir)
            else:
                rel_path = os.path.relpath(path)
            bak_path = os.path.join(glb.config['dir']['bak_dir'], rel_path)
            upload_path = os.path.normpath(rel_path)
            upload_dir = glb.config['dir']['oss_dir']
            if upload_dir:
                upload_path = '/'.join((upload_dir, upload_path))
            logger.info('upload_one(): upload %s ==> %s', path, upload_path)
            try:
                cls._bucket.put_object_from_file(upload_path, path)
            except OssError as err:
                logger.exception('upload_one(): upload %s ==> %s. OssError: %s',
                                 path, upload_path, err)
            else:
                move(path, bak_path)
                with cls._file_lock:
                    cls._files.pop(path)
                logger.info('upload_one(): backup %s ==> %s', path, bak_path)
        except Exception:
            logger.exception('upload_one(path=%s)', path)
            raise
        finally:
            logger.debug('upload_one() <<<')
