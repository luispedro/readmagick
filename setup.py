# -*- coding: utf-8 -*-
# Copyright (C) 2008  Murphy Lab
# Carnegie Mellon University
# 
# Written by Luis Pedro Coelho <luis@luispedro.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# For additional information visit http://murphylab.web.cmu.edu or
# send email to murphy@cmu.edu

import subprocess
from numpy.distutils.core import setup, Extension

def popen3(cmd):
    p = subprocess.Popen(cmd, shell=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    return p.stdout, p.stdin, p.stderr

def readmagick_args(verbose=True):
    def _execute(opts):
        output,input,error = popen3('pkg-config ImageMagick++ %s' % opts)
        errors = error.read()
        if errors:
            output,input,error = popen3('ImageMagick++-config %s' % opts)
            errors += error.read()
        if errors:
            if verbose:
                print '''
Could not find ImageMagick++ headers using
pkg-config or ImageMagick++-config.

Error was: %s

readmagick will not be built.
    ''' % errors
            raise ValueError
        tokens = output.readline().split()
        input.close()
        output.close()
        return tokens
    try:
        libstokens = _execute('--libs')
        cflagstokens = _execute('--cflags')
        return {
            'libraries'    : [t[2:] for t in libstokens if t.startswith('-l')],
            'library_dirs' : [t[2:] for t in libstokens if t.startswith('-L')],
            'include_dirs' : [t[2:] for t in cflagstokens if t.startswith('-I')],
        }
    except:
        return None

long_description = '''ReadMagick

Read and write images using ImageMagick++.

Supports modern image formats such as JPEG2000.
'''
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Programming Language :: C++',
    'Topic :: Scientific/Engineering',
    ]


readmagick = Extension('readmagick', sources = ['readmagick/readmagick.cpp'],  **readmagick_args())
setup(name = 'readmagick',
      version = '1.0.5',
      description = 'Read and write images using ImageMagick',
      long_description = long_description,
      classifiers = classifiers,
      author = 'Luis Pedro Coelho',
      author_email = 'luis@luispedro.org',
      license = 'GPL',
      ext_modules = [readmagick]
      )

