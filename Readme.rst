cython-hidapi
=============

.. contents::

Description
-----------

A cython interface to the hidapi from https://github.com/signal11/hidapi with the C modification for windows from http://code.google.com/p/picusb/downloads/detail?name=hidapi_git_mingw_7e93a4e068825d227807.zip&can=2&q= so I could build it with mingw on windows.

This has been tested with::
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

    $ git clone https://github.com/gbishop/cython-hidapi.git
    $ cd cython-hidapi
    
For other download options (zip, tarball) visit the github web page of `cython-hidapi <https://github.com/gbishop/cython-hidapi>`_

2. Build cython-hidapi extension module for your platform::

    $ python setup[-mac|-windows].py build

3. Install cython-hidapi module into your Python distribution::
  
    $ [sudo] python setup[-mac|-windows].py install
    
3. Test install::

    $ python
    >>> import hid
    >>>
    
5. Try example script::

    $ python try.py
