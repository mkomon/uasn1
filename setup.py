#
# This file is part of uASN1. uASN1 is free software that is
# made available under the MIT license. Consult the file "LICENSE" that
# is distributed together with this file for the exact licensing terms.
#
# uASN1 is copyright (c) 2007-2021 by the uASN1 authors. See the
# file "AUTHORS" for a complete overview.

import sys

# Support both setuptools (if installed) and distutils
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

classifiers = \
[
    'Development Status :: 4 - Beta',
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

args = \
{
    'name': 'uasn1',
    'version': '0.1',
    'description': 'An ASN1 encoder/decoder for MicroPython',
    'author': 'Martin Komon',
    'author_email': 'martin@mkomon.cz',
    'package_dir': {'': 'lib'},
    'py_modules': ['uasn1']
}

if sys.version_info[:3] >= (3, 4, 0):
    args['classifiers'] = classifiers

setup(**args)
