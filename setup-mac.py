from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
os.environ['CFLAGS'] = "-framework IOKit -framework CoreFoundation"
os.environ['LDFLAGS'] = ""

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("hid", ["hid.pyx", "hid-mac.c"])]
)
