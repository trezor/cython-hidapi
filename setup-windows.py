from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
#os.environ['CFLAGS'] = "-I/usr/include/libusb-1.0"
#os.environ['LDFLAGS'] = "-lsetupapi"

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("hid", ["hid.pyx", "hid-windows.c"],
                             libraries=["setupapi"])]
)
