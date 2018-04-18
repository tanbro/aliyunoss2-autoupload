#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setuptools script file
"""

from __future__ import absolute_import, unicode_literals

from setuptools import setup, find_packages

setup(
    name='aliyunoss2-autoupload',
    namespace_packages=[],
    packages=find_packages('src'),
    package_dir={'': 'src'},

    description='Watch files in a directory and upload them to Aliyun OSS on file writing completed',
    url='https://github.com/tanbro/aliyunoss2-autoupload',
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    license='AGPLv3+',
    keywords='aliyun oss autoupload',

    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
    },
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],

    install_requires=[
        'argparse;python_version<"2.7"',
        'enum34;python_version<"3.4"',
        'futures;python_version<"3.0"',
        'oss2',
        'PyYAML',
    ],

    python_requires='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',

    entry_points={
        'console_scripts': [
            'aliyunoss2-autoupload = aliyunoss2_autoupload.__main__:main',
        ],
    },

    extras_require={},

    package_data={
        '': ['data/*/*']
    },

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet',
        'Topic :: Communications :: File Sharing',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
