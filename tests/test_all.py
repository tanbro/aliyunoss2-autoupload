from __future__ import absolute_import, unicode_literals, print_function

import os
import shutil
import sys
import unittest
from time import sleep

from dotenv import load_dotenv

from aliyunoss2_autoupload import conf, glb
from aliyunoss2_autoupload.performer import Performer

_PYTHON_VERSION_MAYOR_MINOR = '{0[0]}.{0[1]}'.format(sys.version_info)

load_dotenv()


class OssAutoUploadTestCase(unittest.TestCase):
    def setUp(self):
        os.makedirs('tests/conf')
        cfg_files = {
            'log': 'tests/conf/log.yml',
            'prog': 'tests/conf/prog.yml',
        }
        for conf_name, conf_file in cfg_files.items():
            with open(conf_file, 'w') as f:
                conf.print_config(conf_name, f)
        conf.load_logging_config(cfg_files['log'])
        conf.load_program_config(cfg_files['prog'])
        # Fake OSS config
        glb.config['oss'] = dict(
            name=os.environ.get('OSS_NAME'),
            endpoint=os.environ.get('OSS_ENDPOINT'),
            access_key_id=os.environ.get('OSS_ACCESS_KEY_ID'),
            access_key_secret=os.environ.get('OSS_ACCESS_KEY_SECRET'),
        )
        #
        Performer.initial()

    def tearDown(self):
        Performer.release()
        shutil.rmtree('tests/conf')

    def test_upload_one(self):
        # Fake watcher config
        key = 'tests/uploads/1.dat'
        glb.config['watcher']['patterns'] = 'tests/uploads/*'
        glb.config['watcher']['write_complete_time'] = 0.1
        # generate a random binary file and upload
        os.makedirs('tests/uploads')
        try:
            with open(key, 'wb') as f:
                f.write(os.urandom(1024))  # replace 1024 with size_kb if not unreasonably large
            # wait for `write_complete_time`
            sleep(0.1)
            # scan and upload
            Performer.run_once()
        finally:
            shutil.rmtree('tests/uploads')

        # check if uploaded path ok
        bucket = Performer._get_oss_bucket()
        self.assertTrue(bucket.object_exists(key))
        bucket.delete_object(key)

    def test_upload_many(self):
        # Fake watcher config
        keys = []
        for i in range(10):
            keys.append(os.path.join('tests', 'uploads', '{0}.dat'.format(i)))
        glb.config['watcher']['patterns'] = 'tests/uploads/*'
        glb.config['watcher']['write_complete_time'] = 0.1
        # generate a random binary file and upload
        os.makedirs('tests/uploads')
        try:
            for key in keys:
                with open(key, 'wb') as f:
                    f.write(os.urandom(1024))  # replace 1024 with size_kb if not unreasonably large
            # wait for `write_complete_time`
            sleep(0.1)
            # scan and upload
            Performer.run_once()
        finally:
            shutil.rmtree('tests/uploads')

        # check if uploaded path ok
        bucket = Performer._get_oss_bucket()
        for key in keys:
            self.assertTrue(bucket.object_exists(key))
        bucket.batch_delete_objects(keys)

    if _PYTHON_VERSION_MAYOR_MINOR >= '3.5':

        def test_upload_recursive(self):
            # Fake watcher config
            keys = []
            for i in range(10):
                os.makedirs(os.path.join('tests', 'uploads', '{0}'.format(i)))
                keys.append(os.path.join('tests', 'uploads', '{0}.dat'.format(i)))
                for j in range(10):
                    dir_name = os.path.join('tests', 'uploads', '{0}'.format(i))
                    if not os.path.isdir(dir_name):
                        os.makedirs(dir_name)
                    keys.append(os.path.join('tests', 'uploads', '{0}'.format(i), '{0}.dat'.format(j)))
            glb.config['watcher']['patterns'] = 'tests/uploads/**/*'
            glb.config['watcher']['recursive'] = True
            glb.config['watcher']['write_complete_time'] = 0.1
            # generate a random binary file and upload
            os.makedirs('tests/uploads', exist_ok=True)
            try:
                for key in keys:
                    with open(key, 'wb') as f:
                        f.write(os.urandom(1024))  # replace 1024 with size_kb if not unreasonably large
                # wait for `write_complete_time`
                sleep(1)
                # scan and upload
                Performer.run_once()
            finally:
                shutil.rmtree('tests/uploads')

            # check if uploaded path ok
            bucket = Performer._get_oss_bucket()
            for key in keys:
                self.assertTrue(bucket.object_exists(key))
            bucket.batch_delete_objects(keys)


if __name__ == '__main__':
    unittest.main()
