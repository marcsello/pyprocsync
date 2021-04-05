==========
PyProcSync
==========


.. image:: https://img.shields.io/pypi/v/pyprocsync.svg
        :target: https://pypi.python.org/pypi/pyprocsync

.. image:: https://img.shields.io/travis/marcsello/pyprocsync.svg
        :target: https://travis-ci.com/marcsello/pyprocsync

.. image:: https://readthedocs.org/projects/pyprocsync/badge/?version=latest
        :target: https://pyprocsync.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Synchronize events between processes over the network.
This package provides similar behaviour as Python's `threading.Event` but it is designed to be used with multiple processes running on different computers.

An example use-case might be controlling multiple industrial robots where timing is critical.


* Free software: MIT license
* Documentation: https://pyprocsync.readthedocs.io



Features
--------

* Supports multiple backends (Currently implemented: Redis)
* About 1ms precision (see docs.)
* Synchronize events based on system clock (NTP is a must have)

Example
--------


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
