from __future__ import absolute_import, print_function

import io
import os
import shutil
import sys
import unittest

import yaml
from dotenv import load_dotenv

from aliyunoss2_autoupload import __main__ as main_module
from aliyunoss2_autoupload import conf
from aliyunoss2_autoupload.performer import Performer
from aliyunoss2_autoupload.utils.strhelper import to_unicode

_PYTHON_VERSION_MAYOR_MINOR = '{0[0]}.{0[1]}'.format(sys.version_info)

load_dotenv()

str_ver = '{0[0]}.{0[1]}-{1}'.format(sys.version_info, sys.platform)


class RunOnceTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RunOnceTestCase, self).__init__(*args, **kwargs)
        self.conf_buf = None  # type: io.StringIO

    def setUp(self):

        # prog.yml
        with io.StringIO() as stream:
            conf.print_config('prog', stream)
            data = yaml.safe_load(stream.getvalue())
        # Fake OSS config
        data['oss'] = dict(
            name=os.environ.get('OSS_NAME'),
            endpoint=os.environ.get('OSS_ENDPOINT'),
            access_key_id=os.environ.get('OSS_ACCESS_KEY_ID'),
            access_key_secret=os.environ.get('OSS_ACCESS_KEY_SECRET'),
        )
        # Fake load
        with io.StringIO(to_unicode(yaml.safe_dump(data))) as stream:
            stream.seek(0)
            conf.load_program_config(stream)

        # Fake arguments
        main_module.parse_arguments(['run', '--only-once'])

        # log.yml
        log_conf_buf = io.StringIO()
        conf.print_config('log', log_conf_buf)
        log_conf_buf.seek(0)
        main_module._arguments.logging_config_file = log_conf_buf

        # prog.yml
        with io.StringIO() as stream:
            conf.print_config('prog', stream)
            self.conf_data = yaml.safe_load(stream.getvalue())
        # Fake OSS config
        self.conf_data['oss'] = dict(
            name=os.environ.get('OSS_NAME'),
            endpoint=os.environ.get('OSS_ENDPOINT'),
            access_key_id=os.environ.get('OSS_ACCESS_KEY_ID'),
            access_key_secret=os.environ.get('OSS_ACCESS_KEY_SECRET'),
        )
        # Fake load
        self.set_conf_data()

    def set_conf_data(self):
        self.conf_buf = io.StringIO(to_unicode(yaml.safe_dump(self.conf_data)))
        self.conf_buf.seek(0)
        main_module._arguments.config_file = self.conf_buf

    def tearDown(self):
        Performer.release()

    def test_upload_many(self):
        # Fake watcher config
        keys = []
        upload_dir = os.path.join('tests', 'uploads', str_ver)
        os.makedirs(upload_dir)
        for i in range(5):
            file_name = os.path.join(upload_dir, '{0}.dat'.format(i))
            keys.append(file_name)
        self.conf_data['watcher']['patterns'] = upload_dir + '/*.dat'
        self.conf_data['watcher']['write_complete_time'] = 0.1
        self.set_conf_data()
        # generate a random binary file and upload
        try:
            for key in keys:
                with open(key, 'wb') as f:
                    f.write(os.urandom(1024))  # replace 1024 with size_kb if not unreasonably large
            # scan and upload
            main_module.main()
        finally:
            shutil.rmtree(upload_dir)

        # check if uploaded path ok
        bucket = Performer._get_oss_bucket()
        for key in keys:
            self.assertTrue(bucket.object_exists(key))
        bucket.batch_delete_objects(keys)

    if _PYTHON_VERSION_MAYOR_MINOR >= '3.5':

        def test_upload_recursive(self):
            # Fake watcher config
            keys = []
            upload_dir = os.path.join('tests', 'uploads', str_ver)
            os.makedirs(upload_dir)
            for i in range(3):
                file_name = os.path.join(upload_dir, '{0}.dat'.format(i))
                keys.append(file_name)
                for j in range(2):
                    dir_name = os.path.join(upload_dir, '{0}'.format(i))
                    file_name = os.path.join(dir_name, '{0}.dat'.format(j))
                    if not os.path.isdir(dir_name):
                        os.makedirs(dir_name)
                    keys.append(file_name)
            self.conf_data['watcher']['patterns'] = upload_dir + '/**/*.dat'
            self.conf_data['watcher']['recursive'] = True
            self.conf_data['watcher']['write_complete_time'] = 0.1
            self.set_conf_data()
            # generate a random binary file and upload
            try:
                for key in keys:
                    with open(key, 'wb') as f:
                        f.write(os.urandom(1024))  # replace 1024 with size_kb if not unreasonably large
                # scan and upload
                main_module.main()
            finally:
                shutil.rmtree(upload_dir)

            # check if uploaded path ok
            bucket = Performer._get_oss_bucket()
            for key in keys:
                self.assertTrue(bucket.object_exists(key))
            bucket.batch_delete_objects(keys)


if __name__ == '__main__':
    unittest.main()
