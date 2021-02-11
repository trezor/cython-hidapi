cython-hidapi
=============

.. contents::

Description
-----------

A Cython interface to `HIDAPI <https://github.com/libusb/hidapi>`_ library.

This has been tested with:

* `TREZOR <https://trezor.io/>`_ Hardware Wallet
* the PIC18F4550 on the development board from CCS with their example program
* the Fine Offset WH3081 Weather Station

It works on Linux, Windows and macOS.

Software Dependencies
---------------------

* `Python <http://python.org>`_
* `Cython <http://cython.org>`_
* hidraw or libusb+libudev on Linux

License
-------

cython-hidapi may be used by one of three licenses as outlined in LICENSE.txt

Install
-------

::

    $ sudo apt-get install python-dev libusb-1.0-0-dev libudev-dev
    $ sudo pip install --upgrade setuptools
    $ sudo pip install hidapi

For other download options visit the `PyPi page <https://pypi.python.org/pypi/hidapi/>`_.

Build from source
-----------------

1. Download cython-hidapi archive::

    $ git clone https://github.com/trezor/cython-hidapi.git
    $ cd cython-hidapi

2. Initialize hidapi submodule::

    $ git submodule update --init

3. Build cython-hidapi extension module::

    $ python setup.py build

   To use hidraw API instead of libusb add --without-libusb option::

    $ python setup.py build --without-libusb

4. Install cython-hidapi module into your Python distribution::

    $ sudo python setup.py install

   **Alternatively**, you can run pip directly, which will call the necessary build and install commands::

    $ pip install -e .

5. Test install::

    $ python
    >>> import hid
    >>>

6. Try example script::

    $ python try.py

Udev rules
----------

For correct functionality under Linux, you need to create a rule file similar
to `this one <https://raw.githubusercontent.com/trezor/trezor-common/master/udev/51-trezor.rules>`_
in your udev rules directory.

Also you might need to call ``udevadm control --reload-rules`` to reload the rules.

Documentation
-------------

Documentation can be built using Sphinx::

   $ cd docs && make html

The HTML output will be in ``docs/_build/html``.

The documentation is extracted from the code using ``autodoc``.

Note that the build output is used. So rebuilt the package before generating documentation.

Built documentation is also deployed to: `https://trezor.github.io/cython-hidapi/ <https://trezor.github.io/cython-hidapi/>`_.
