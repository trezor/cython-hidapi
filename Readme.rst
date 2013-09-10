cython-hidapi
=============

.. contents::

Description
-----------

A Cython interface to the HIDAPI from https://github.com/signal11/hidapi

This has been tested with:

* the PIC18F4550 on the development board from CCS with their example program.
* the Fine Offset WH3081 Weather Station.

It works on Linux, Windows XP and OS X.


Software Dependencies
---------------------

* Python (http://python.org/download/)
* Cython (http://cython.org/#download)


License
-------
You are free to use cython-hidapi code for any purpose.


Install
-------

1. Download cython-hidapi archive::

    $ git clone https://github.com/trezor/cython-hidapi.git
    $ cd cython-hidapi

For other download options (zip, tarball) visit the github web page of `cython-hidapi <https://github.com/trezor/cython-hidapi>`_

2. Initialize hidapi submodule::

    $ git submodule init
    $ git submodule update

3. Build cython-hidapi extension module::

    $ python setup.py build

4. Install cython-hidapi module into your Python distribution::

    $ [sudo] python setup.py install

5. Test install::

    $ python
    >>> import hid
    >>>

6. Try example script::

    $ python try.py
