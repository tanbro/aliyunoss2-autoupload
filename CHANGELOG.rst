Changelog
*********

0.1
===

Added
-----
* Reload configuration every time before scanning files.
* `--only-once` command line option.

Optimized
---------
* test case for ``main()`` function

0.1b2
=====

:Date: 2018-06-20

Adds
----
* More detailed documents.

Bug Fixes:
----------
* Remove files in `.gitignore`, but tracked.

0.1b1
=====

:Date: 2018-06-19

Changes
-------
* Support old `Python 2.7`, `Python 3.4`
* Config file name extension changed from ``".yaml"`` to ``".yml"``
* Default config file environment variable name
* Default config file path if no environment variable

Adds
----
* Some simple test cases
* CircleCI
* Codacy

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
