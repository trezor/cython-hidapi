cython-hidapi
=============

.. image:: https://travis-ci.org/trezor/cython-hidapi.svg?branch=master
    :target: https://travis-ci.org/trezor/cython-hidapi

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
* hidraw or libusb and libudev on Linux

License
-------
cython-hidapi may be used by one of three licenses as outlined in LICENSE.txt.


Install
-------

    $ pip install hidapi

For other download options visit the PyPi page of cython-hidapi (https://pypi.python.org/pypi/hidapi/)

Build from source
-----------------

1. Download cython-hidapi archive::

    $ git clone https://github.com/trezor/cython-hidapi.git
    $ cd cython-hidapi

2. Initialize hidapi submodule::

    $ git submodule init
    $ git submodule update

3. Build cython-hidapi extension module::

    $ python setup.py build

   To use hidraw API instead of libusb add --without-libusb option::

    $ python setup.py build --without-libusb

4. Install cython-hidapi module into your Python distribution::

    $ [sudo] python setup.py install

5. Test install::

    $ python
    >>> import hid
    >>>

6. Try example script::

    $ python try.py
