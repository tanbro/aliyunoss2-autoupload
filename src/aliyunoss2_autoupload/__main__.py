#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import argparse
import os
import sys

from . import glb
from . import version

_parser = None  # type: ArgumentParser


def set_get_arguments():  # type:()->Namespace
    global _parser
    _parser = argparse.ArgumentParser(
        prog=version.NAME, description='Watch files in a directory and upload them to Aliyun OSS on file writing completed')
    _parser.add_argument('--version', action='version',
                         version='%(prog)s {0}'.format(version.__version__))

    subparsers = _parser.add_subparsers(dest='sub_command', description='',
                                        help='<sub_command --help> Print the help of sub-commands')

    parser_run = subparsers.add_parser(
        'run', help='Start to run then program. It will monitor and upload files continuously.')
    parser_run.add_argument('--oss-endpoint', '-p', type=str, required=True,
                            help='Endpoint URL of Aliyun OSS bucket')
    parser_run.add_argument('--oss-name', '-m', type=str, required=True,
                            help='Name of Aliyun OSS bucket')
    parser_run.add_argument('--oss-key-id', '-k', type=str, required=True,
                            help='Access Key ID of Aliyun OSS bucket')
    parser_run.add_argument('--oss-key-secret', '-s', type=str, required=True,
                            help='Access Key Secret of Aliyun OSS bucket')
    parser_run.add_argument('--no-upload-existed', '-e', type=bool, default=True,
                            help='Only upload new created files, NOT upload existed files. (default=(default%s))')
    parser_run.add_argument('--dir', '-d', type=str, default='',
                            help='Parent directory name of the files pattern. (default=CWD)')
    parser_run.add_argument('pattern', type=str,
                            help='Pattern of the files to monitor')
    parser_run.add_argument('backup_dir', type=str,
                            help='Directory to backup uploaded files')

    parser_echo_config_sample = subparsers.add_parser(
        'echo_config_sample', help='Echo configure file sample')
    parser_echo_config_sample.add_argument('config', type=str, choices=['prog', 'log'],
                                           help='Configure file to echo')

    arguments = glb.args = _parser.parse_args()
    return arguments


def main():
    arguments = set_get_arguments()

    if arguments.sub_command == 'run':
        # Run the monitor/uploader
        pass

    elif arguments.sub_command == 'echo_config_sample':
        pass

    else:
        _parser.print_help()


if __name__ == '__main__':
    main()
