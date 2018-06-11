Changelog
*********

develop
=======

:Date: 2018-06-11

Changes
-------
* Support old `Python 2`, including `2.6`, `2.7`


0.1a3
=====
The first ever-usable version.

:Date: 2018-04-18

Changes
-------
* Now Python 3.5+ ONLY, because ``glob.iglob`` has no ``recursive`` argument and ``"**"`` wildcard in lower Python version

Bug Fixes
---------
* Backup directory errors
* OSS exception
