# -*- coding: utf-8 -*-
# Copyright (C) 2008-2009  Murphy Lab
# Carnegie Mellon University
# 
# Written by Luís Pedro Coelho <lpc@cmu.edu>
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
from os.path import exists
from os import unlink
import numpy
from readmagick import readimg, writeimg
from nose.tools import with_setup

def write_readback(C,fname):
    C = C.copy()
    writeimg(C,fname)
    C2 = readimg(fname)
    return C, C2


_PNG = '/tmp/pyslic_test_file.png'
_TIFF = '/tmp/pyslic_test_file.tiff'
def delete_tmps():
    if exists(_PNG): unlink(_PNG)
    if exists(_TIFF): unlink(_TIFF)

@with_setup(None,delete_tmps)
def test_uint8_color():
    A = numpy.array([
        [[0,1,2],[1,2,3],[2,3,4]],
        [[5,5,5],[6,6,6],[7,7,7]]
        ],
        numpy.uint8)
    B = numpy.array([
        [0,1,2,3,4],
        [5,5,5,5,5]
        ],
        numpy.uint8)
    C = numpy.array([
        [[0,1,2],[1,2,3],[2,3,4]],
        [[5,5,5],[6,6,6],[7,7,7]],
        [[257,257,257],[256,256,256],[707,707,707]]
        ],
        numpy.uint16)
    D = numpy.array([
        [0,1,2,3,4],
        [5,5,5,5,5],
        [258,258,258,258,258]
        ],
        numpy.uint16)
    def test_one(C,fname,correct):
        writeimg(C,fname)    
        C,C2 = write_readback(C,fname)
        if correct: C2 //= 257
        assert C.shape == C2.shape
        assert numpy.all(C == C2)
    yield test_one, A, _PNG, True
    yield test_one, A[::-1,::-1,:], _PNG, True
    yield test_one, B, _PNG, True
    yield test_one, C, _TIFF, False
    yield test_one, D, _TIFF, False

