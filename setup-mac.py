from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
os.environ['CFLAGS'] = "-framework IOKit -framework CoreFoundation -I"  + os.path.join(os.getcwd(), "hidapi", "hidapi")
os.environ['LDFLAGS'] = ""

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("hid", ["hid.pyx", os.path.join(os.getcwd(), "hidapi", "mac", "hid.c")])]
)
