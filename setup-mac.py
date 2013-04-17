from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
os.environ['CFLAGS'] = "-I"  + os.path.join(os.getcwd(), "hidapi", "hidapi")
os.environ['LDFLAGS'] = "-framework IOKit -framework CoreFoundation"

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("hid", ["hid.pyx", os.path.join(os.getcwd(), "hidapi", "mac", "hid.c")])]
)
