A cython interface to the hidapi from https://github.com/signal11/hidapi with the C modification for windows from http://code.google.com/p/picusb/downloads/detail?name=hidapi_git_mingw_7e93a4e068825d227807.zip&can=2&q= so I could build it with mingw on windows.

I only wrapped the functions I needed to get the job done. 

This has been tested with the PIC18F4550 on the development board from CCS with their example program. It works on Linux and Windows XP. 

You are free to use it for any purpose.

