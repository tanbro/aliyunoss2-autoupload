:Source: https://github.com/tanbro/aliyunoss2-autoupload
:Package: https://pypi.org/project/aliyunoss2-autoupload/

|Circle CI| |Codacy| |Codacy Coverage| |PYPI Version| |PYPI License| |PYPI Python Versions| |PYPI Status| |PYPI Format|

aliyunoss2-autoupload
#####################

Monitor files by wildcard patterns, upload them to ALIYUN OSS, then move to backup directory.

Usages
******

After the package installed, run the command in a terminator, show help messages::

    $ aliyunoss2-autoupload --help
    usage: aliyunoss2-autoupload [-h] [--version] {run,echo_config_sample} ...

    Watch files in a directory and upload them to Aliyun OSS on file writing
    completed

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit

    subcommands:

      {run,echo_config_sample}
                            <sub_command --help> Print the help of sub_commands
        run                 Start to run then program. It will monitor and upload
                            files continuously.
        echo_config_sample  Echo configure file sample

::

    $ aliyunoss2-autoupload run --help
    usage: aliyunoss2-autoupload run [-h] [--config-file CONFIG_FILE]
                                    [--logging-config-file LOGGING_CONFIG_FILE]

    optional arguments:
    -h, --help            show this help message and exit
    --config-file CONFIG_FILE, -c CONFIG_FILE
                            The program configuration file. The program will first
                            try to load configuration file from environment
                            variable ${ALIYUNOSS2_AUTOUPLOAD_CONF}. If the
                            environment variable not assigned, then try to load
                            configuration file from
                            "conf/aliyunoss2-autoupload.yml"
    --logging-config-file LOGGING_CONFIG_FILE, -l LOGGING_CONFIG_FILE
                            The logging configuration file. The program will first
                            try to load configuration file from environment
                            variable ${ALIYUNOSS2_AUTOUPLOAD_LOG_CONF}. If the
                            environment variable not assigned, then try to load
                            configuration file from
                            "conf/aliyunoss2-autoupload.log.yml"

.. code-block:: console

    $ aliyunoss2-autoupload echo_config_sample --help
    usage: aliyunoss2-autoupload echo_config_sample [-h] {prog,log}

    positional arguments:
    {prog,log}  Configure file to echo

    optional arguments:
    -h, --help  show this help message and exit


------

.. |Circle CI| image:: https://circleci.com/gh/tanbro/aliyunoss2-autoupload.svg?style=svg
    :target: https://circleci.com/gh/tanbro/aliyunoss2-autoupload

.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/2fff1a8c9fd84366bffb92f026862dc2
    :target: https://www.codacy.com/app/tanbro/aliyunoss2-autoupload?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tanbro/aliyunoss2-autoupload&amp;utm_campaign=Badge_Grade

.. |Codacy Coverage| image:: https://api.codacy.com/project/badge/Coverage/2fff1a8c9fd84366bffb92f026862dc2
    :target: https://www.codacy.com/app/tanbro/aliyunoss2-autoupload?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tanbro/aliyunoss2-autoupload&amp;utm_campaign=Badge_Coverage

.. |PYPI Version| image:: https://img.shields.io/pypi/v/aliyunoss2-autoupload.svg
    :target: https://pypi.org/project/aliyunoss2-autoupload/

.. |PYPI License| image:: https://img.shields.io/pypi/l/aliyunoss2-autoupload.svg
    :target: https://pypi.org/project/aliyunoss2-autoupload/

.. |PYPI Python Versions| image:: https://img.shields.io/pypi/pyversions/aliyunoss2-autoupload.svg
    :target: https://pypi.org/project/aliyunoss2-autoupload/

.. |PYPI Status| image:: https://img.shields.io/pypi/status/aliyunoss2-autoupload.svg
    :target: https://pypi.org/project/aliyunoss2-autoupload/

.. |PYPI Format| image:: https://img.shields.io/pypi/format/aliyunoss2-autoupload.svg
    :target: https://pypi.org/project/aliyunoss2-autoupload/
