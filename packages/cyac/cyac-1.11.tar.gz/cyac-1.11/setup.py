#!/usr/bin/env python3

from setuptools import setup
from distutils.extension import Extension

# Delayed import; https://stackoverflow.com/questions/37471313/setup-requires-with-cython
try:
    from Cython.Build import cythonize
except ImportError:
     def cythonize(*args, **kwargs):
         from Cython.Build import cythonize
         return cythonize(*args, **kwargs)

# import os
# os.environ['CFLAGS'] = '-O0'
try:
    long_description = open("README.md", encoding="utf8").read()
except IOError:
    long_description = ""

setup(
    version="1.11",
    description="High performance Trie and Ahocorasick automata (AC automata) for python",
    name="cyac",
    url="https://github.com/nppoly/cyac",
    author="nppoly",
    author_email="nppoly@foxmail.com",
    packages=["cyac"],
    package_dir={'cyac': 'lib/cyac'},
    package_data={'cyac': ['*.pxd', 'unicode_portability.c', 'unicodetype_db.h']},
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=['cython>=0.29.0', 'Cython>=0.29.0'],
    setup_requires=['Cython'],
    ext_modules = cythonize([
        "lib/cyac/util.pyx",
        "lib/cyac/utf8.pyx",
        "lib/cyac/xstring.pyx",
        "lib/cyac/trie.pyx",
        "lib/cyac/ac.pyx"]),
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        "Programming Language :: Python",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ]
)
